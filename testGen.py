# pip install accelerate
from transformers import AutoTokenizer, AutoModelForCausalLM
import time
import requests
import json

accessToken = "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"

# """
# {host: {port: {worked: [CVE], not_worked: [CVE]}}}
# """

# cveList = ["CVE-2012-0814", "CVE-2008-1657", "CVE-2011-2168", "CVE-2011-4327","CVE-2008-5161","CVE-2010-4478","CVE-2011-5000","CVE-2008-3259","CVE-2010-5107","CVE-2011-1013", "CVE-2010-4754", "CVE-2010-4755"]

# cveList = [
#      "CVE-2014-0231",
#      "CVE-2009-1891",
#      "CVE-2012-2687",
#      "CVE-2009-3094",
#      "CVE-2016-4975",
#      "CVE-2008-0456",
#      "CVE-2017-9798",
#      "CVE-2008-2364",
#      "CVE-2016-8743",
#      "CVE-2014-0226",
#      "CVE-2011-441",
#      "CVE-2017-3167",
#      "CVE-2013-6438",
#      "CVE-2012-4558",
#      "CVE-2009-1956",
#      "CVE-2012-0031",
#      "CVE-2014-0098",
#      "CVE-2012-3499",
#      "CVE-2009-1195",
#      "CVE-2011-4317",
#      "CVE-2011-3368",
#      "CVE-2017-7679",
#      "CVE-2009-0023",
#      "CVE-2009-2699",
#      "CVE-2012-0883",
#      "CVE-2013-1896",
#      "CVE-2014-0118",
#      "CVE-2012-0053",
#      "CVE-2010-1623",
#      "CVE-2011-3192",
#      "CVE-2009-1890",
#      "CVE-2015-3183",
#      "CVE-2013-5704",
#      "CVE-2007-6750",
#      "CVE-2016-5387",
#      "CVE-2009-3560",
#      "CVE-2008-2939",
#      "CVE-2009-3555",
#      "CVE-2010-1452",
#      "CVE-2010-0408",
#      "CVE-2011-3639",
#      "CVE-2017-9788",
#      "CVE-2010-0434",
#      "CVE-2011-4415",
#      "CVE-2008-0005",
#      "CVE-2008-0455",
#      "CVE-2013-1862",
#      "CVE-2009-3095",
#      "CVE-2011-3607"
# ]

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
     # Generate a markedown table for each port
     table = f"\n| Exploit Name | {vulner.get('exploit')} |\n| --- | --- |\n"
     if vulner.get("exploit_options"):
          options = vulner.get("exploit_options")
          for option_name in options.keys():
               table += f"| {option_name} | {str(options.get(option_name))} |\n"
          
     if vulner.get("payload"):
          table += f"\n| Payload Name | {vulner.get('payload')} |\n| --- | --- |\n"
     
     if vulner.get("payload_description"):
          table += f"| Payload Description | {vulner.get('payload_description')} |\n"

     if vulner.get("payload_options"):
          options = vulner.get("payload_options")
          for option_name in options.keys():
               table += f"| {option_name} | {str(options.get(option_name))} |\n"
     return table


def getDescription(exploits: dict) -> tuple[list, list, list]:
     # Get the desciption from a dictionary that contain output from metasploit
     # Can also get CVSS score if there is CVE number
     descriptions = []
     CVSS = []
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
     text = ""
     for i in range(len(descriptions)):
          text += f"{descriptions[i]}\n"
          if CVSS[i][0]:
               text += f"* Its CVE number is {CVSS[i][0]}.\n"
          if CVSS[i][1]:
               text += f"* Its CVSS score is {CVSS[i][1]}.\n"
          if CVSS[i][2]:
               text += f"* Its CVSS vector is {CVSS[i][2]}\n"
          text += tables[i]
     return text

def generateSectionReport(sectionResult: dict, tokenizer:AutoTokenizer, model:AutoModelForCausalLM)->str:
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
     report = ""
     for IP in exploitResult.keys():
          exploit_IP = exploitResult.get(IP)
          report += f"# Penetration testing for {IP}\n\n"
          for port in exploit_IP.keys():
               exploit_port = exploit_IP.get(port)
               report += f"## Port {port}\n"
               shell_exploits = {}
               failed_exploits = {}
               for exploit in exploit_port.keys():
                    status = exploit_port[exploit].get("status")
                    if status and status == "ACQUIRED_SHELL":
                         shell_exploits[exploit] = exploit_port[exploit]
                    else:
                         failed_exploits[exploit] = exploit_port[exploit]
               if len(shell_exploits) > 0:
                    report += "### Vulnerabilities that we exploited to get a shell\n"
                    report += generateSectionReport(shell_exploits, tokenizer, model)
                    report += "\n"
               if len(failed_exploits) > 0:
                    report += "### Vulnerabilities that we are unable to exploit\n"
                    report += generateSectionReport(failed_exploits, tokenizer, model)
                    report += "\n"
               print(f"Port {port} completed")
               # return report
     return report

if __name__ == "__main__":
     exploit = loadJSON("app/seed/exploit/metasploitable.json")
     pretrained = "google/gemma-2b-it"
     tokenizer = AutoTokenizer.from_pretrained(pretrained, token=accessToken)
     model = AutoModelForCausalLM.from_pretrained(pretrained, device_map="auto", token=accessToken)
     result = generateReport(exploit, tokenizer, model)
     outputFile = open("mlOutput.md", "w")
     outputFile.write(result)
     outputFile.close()
     print("Finished")