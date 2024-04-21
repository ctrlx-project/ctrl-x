# pip install accelerate
from transformers import AutoTokenizer, AutoModelForCausalLM
import time
import requests
import json
from models import db, Exploit, Report
from celery import shared_task

accessToken = "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"

def loadJSON(filepath:str)->dict:
    # Load JSON file into a dictionary
    try:
        f = open(filepath, "r")
    except:
        print("File does not exist")
        exit(1)
    dict = json.load(f)
    return dict

def getTable(vulner: dict)->str:
     # Generate a markedown table for each vulnerability
     table = [f"\n| Exploit Name | {vulner.get('exploit')} |\n| --- | --- |\n"]
     if vulner.get("exploit_options"):
          options = vulner.get("exploit_options")
          for option_name in options.keys():
               table.append(f"| {option_name} | {str(options.get(option_name))} |\n")
          
     if vulner.get("payload"):
          table.append(f"\n| Payload Name | {vulner.get('payload')} |\n| --- | --- |\n")
     
     if vulner.get("payload_description"):
          table.append(f"| Payload Description | {vulner.get('payload_description')} |\n")

     if vulner.get("payload_options"):
          options = vulner.get("payload_options")
          for option_name in options.keys():
               table.append(f"| {option_name} | {str(options.get(option_name))} |\n")
     table.append("\n")
     return "".join(table)


def getDescription(exploits: dict) -> tuple[list, list, list]:
     # Get the desciption from a dictionary that contain output from metasploit for a port
     # Can also get CVSS score if there is CVE number
     descriptions = []
     CVSS = [] # A list of list, inner list is [CVE, CVSS score, CVSS vector]
     tables = []
     remaining = len(exploits)
     for exploitName in exploits.keys():
          exploit = exploits.get(exploitName)
          tables.append(getTable(exploit))
          cve = exploit.get("CVE")
          remaining -= 1
          if cve:
               r = requests.get(f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve}")
               if remaining > 0:
                    time.sleep(5)
               try:
                    r_dict = r.json()
               except:
                    descriptions.append(exploit.get("exploit_description"))
                    CVSS.append([None, None, None])    
                    continue
               vulnerabilities = r_dict.get("vulnerabilities")
               if vulnerabilities and len(vulnerabilities) == 1:
                    cveData = vulnerabilities[0].get("cve")
                    curDescription = ""
                    if cveData:
                         if cveData.get("descriptions"):
                              descriptionList = cveData.get("descriptions")
                              for description in descriptionList:
                                   if description.get("lang") == "en" and description.get("value") is not None:
                                        curDescription += description.get("value") 
                         else:
                              descriptions.append(exploit.get("exploit_description"))
                         addCVSS = False
                         if cveData.get("metrics"):
                              metric = cveData.get("metrics")
                              if len(metric.keys()) > 0:
                                   cvssMetric = metric.get(list(metric.keys())[0])
                                   if len(cvssMetric) > 0:
                                        cvssData = cvssMetric[0].get("cvssData")
                                        if cvssData and cvssData.get("vectorString") and cvssData.get("baseScore"):
                                             CVSS.append([cve, cvssData.get("baseScore"), cvssData.get("vectorString")]) 
                                             addCVSS = True  
                         if not addCVSS:
                              CVSS.append([cve, None, None])
                    descriptions.append(curDescription)
               else:
                    descriptions.append(exploit.get("exploit_description"))
                    CVSS.append([None, None, None])
          else:
               descriptions.append(exploit.get("exploit_description"))
               CVSS.append([None, None, None])
     return descriptions, CVSS, tables

def descriptionToMD(descriptions:list, CVSS: list, tables: list) -> str:
     text = []
     for i in range(len(descriptions)):
          text.append(f"{descriptions[i]}\n")
          if CVSS[i][0]:
               text.append(f"\n* Its CVE number is {CVSS[i][0]}.\n")
          if CVSS[i][1]:
               text.append(f"* Its CVSS score is {CVSS[i][1]}.\n")
          if CVSS[i][2]:
               text.append(f"* Its CVSS vector is {CVSS[i][2]}\n")
          text.append(tables[i])
     return "".join(text)

def generateSectionReport(sectionResult: dict, tokenizer:AutoTokenizer, model:AutoModelForCausalLM)->str:
     """
     Create the markdown for all the exploited vulnerabilities in a port or all the vulnerabilities that are not exploited in a port
     sectionResult: dictionary containing the exploit result for this section
     tokenizer: tokenizer for the LLM
     model: LLM model
     """
     descriptions, CVSS, tables = getDescription(sectionResult)
     # print(len(descriptions), len(CVSS), len(tables))
     descriptionMD = descriptionToMD(descriptions, CVSS, tables)

     descriptionText = "\n".join(descriptions)

     input_text =  f"""Generate the potential impacts for each of the below vulnerabilities, which is separated by line break:
{descriptionText}

The format should be markdown, where each vulnerability is a bullet point. Text other than heading should not be bolded. Do not provide example. Do not repeat the Potential Impacts heading. 
Generated text starts here:
### Potential Impacts
"""

     separator = "Generated text starts here:"
     end = "<eos>"

     input_ids = tokenizer(input_text, return_tensors="pt").to("cuda").input_ids
     outputs = model.generate(input_ids, max_new_tokens=1000)

     combinedOutput = ""
     combinedOutput += descriptionMD

     result = tokenizer.decode(outputs[0])
     startIndex = result.find(separator) + len(separator)
     endIndex = result.find(end)
     combinedOutput += result[startIndex:endIndex]

     input_text =  f"""Generate mitigation strategies for each of the below vulnerabilities:
{descriptionText}

The format should be markdown, where each vulnerability have a bolded heading that starts with Vulnerability [number]. Text other than heading should not be bolded. Do not give examples.
Generated text starts here:
### Mitigation Strategies
"""

     input_ids = tokenizer(input_text, return_tensors="pt").to("cuda").input_ids
     outputs = model.generate(input_ids, max_new_tokens=1000)
     result = tokenizer.decode(outputs[0])
     startIndex = result.find(separator) + len(separator)
     endIndex = result.find(end)
     combinedOutput += result[startIndex:endIndex]
     
     return combinedOutput

def generateReport(exploitResult: dict, tokenizer:AutoTokenizer, model:AutoModelForCausalLM) -> str:
     """
     Create the markdown report
     exploitResult: dictionary containing the exploit result
     tokenizer: tokenizer for the LLM
     model: LLM model
     """
     report = []
     for IP in exploitResult.keys():
          exploit_IP = exploitResult.get(IP)
          report.append(f"# Penetration testing for {IP}\n\n")
          for port in exploit_IP.keys():
               exploit_port = exploit_IP.get(port)
               report.append(f"## Port {port}\n")
               shell_exploits = {}
               failed_exploits = {}
               for exploit in exploit_port.keys():
                    status = exploit_port[exploit].get("status")
                    if status and status == "ACQUIRED_SHELL":
                         shell_exploits[exploit] = exploit_port[exploit]
                    else:
                         failed_exploits[exploit] = exploit_port[exploit]
               if len(shell_exploits) > 0:
                    report.append("### Vulnerabilities that we exploited to get a shell\n")
                    report.append(generateSectionReport(shell_exploits, tokenizer, model))
                    report.append("\n")
               if len(failed_exploits) > 0:
                    report.append("### Vulnerabilities that we are unable to exploit\n")
                    report.append(generateSectionReport(failed_exploits, tokenizer, model))
                    report.append("\n")
               print(f"Port {port} completed")
               # return report
     return "".join(report)

@shared_task(ignore_result=True, name='report', autoretry_for=(Exception,), retry_backoff=True,
             retry_jitter=True, retry_kwargs={'max_retries': 3})
def report_job(id:int, user:int, ip:str):
     # Takes a report job and save the result into the database.
     exploit = Exploit.query.filter_by(id=id).first()
     exploit_data = json.loads(exploit.exploit_data)
     report = generateReport(exploit_data)
     newReport = Report(user_id=user, ip=ip, content=report)
     db.session.add(newReport)
     db.session.commit()


def main():
     exploit = loadJSON("./seed/exploit/metasploitable.json")
     pretrained = "google/gemma-2b-it"
     tokenizer = AutoTokenizer.from_pretrained(pretrained, token=accessToken)
     model = AutoModelForCausalLM.from_pretrained(pretrained, device_map="auto", token=accessToken)
     result = generateReport(exploit, tokenizer, model)
     outputFile = open("mlOutput.md", "w")
     outputFile.write(result)
     outputFile.close()
     print("Finished")

if __name__ == "__main__":
     main()