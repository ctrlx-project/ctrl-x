# pip install accelerate
from transformers import AutoTokenizer, AutoModelForCausalLM
import time
import requests

accessToken = "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"

# """
# {host: {port: {worked: [CVE], not_worked: [CVE]}}}
# """

cveList = ["CVE-2012-0814", "CVE-2008-1657", "CVE-2011-2168", "CVE-2011-4327","CVE-2008-5161","CVE-2010-4478","CVE-2011-5000","CVE-2008-3259","CVE-2010-5107","CVE-2011-1013", "CVE-2010-4754", "CVE-2010-4755"]

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

# Can also get CVSS score
def getDescription(cveList: list) -> str:
     descriptions = []
     CVSS = []
     for cve in cveList:
          r = requests.get(f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve}")
          time.sleep(5)
          try:
               r_dict = r.json()
          except:
               # print(f"Problem for {cve}: ", r.text)
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
                         continue
                    if cveData.get("metrics"):
                         metric = cveData.get("metrics")
                         addCVSS = False
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
     return descriptions, CVSS

def descriptionToMD(descriptions:list, CVSS: list) -> str:
     text = "# Vulnerabilities\n"
     for i in range(len(descriptions)):
          text += f"* {descriptions[i]}\n\t* Its CVE number is {CVSS[i][0]}.\n"
          if CVSS[i][1]:
               text += f"\t* Its CVSS score is {CVSS[i][1]}.\n"
          if CVSS[i][2]:
               text += f"\t* Its CVSS vector is {CVSS[i][2]}\n"
     return text

# print("Length of CVE: ", len(cveList))
descriptions, CVSS = getDescription(cveList)
# print(CVSS)
# print("Length of CVSS: ", len(CVSS))
# print(descriptions)
print("Finished getting description")

# pretrained = "openchat/openchat_3.5"
pretrained = "google/gemma-2b-it"
# pretrained = "google/gemma-7b-it"
tokenizer = AutoTokenizer.from_pretrained(pretrained, token=accessToken)
model = AutoModelForCausalLM.from_pretrained(pretrained, device_map="auto", token=accessToken)
descriptionText = "\n".join(descriptions)

input_text =  f"""Generate the potential impact for each of the below vulnerabilities as markdown, give each vulnerability a bolded heading:
{descriptionText}
Generated text starts here:
# Potential Impacts
"""

separator = "Generated text starts here:"

# input_text =  f"""Write the executive summary of the penetration testing report for a network with the below vulnerabilities:
# {descriptions}
# Generated text starts here:
# """

# input_text =  f"""Write the conclusion of the penetration testing report for a network with the below vulnerabilities:
# {descriptions}
# Generated text starts here:
# """

# start = time.time()
input_ids = tokenizer(input_text, return_tensors="pt").to("cuda").input_ids
# end = time.time()
# print("Input tokenized: ", end -start)

# start = time.time()
# print("Start model generation")
outputs = model.generate(input_ids, max_new_tokens=1000)
# end = time.time()

# print("Generation time: ", end-start)

# start = time.time()
outputFile = open("mlOutput.md", "w")
outputFile.write(descriptionToMD(descriptions, CVSS))

result = tokenizer.decode(outputs[0])
startIndex = result.find(separator) + len(separator)
outputFile.write(result[startIndex:])
print(result)
# end = time.time()
# print("Output tokenized: ", end -start)

input_text =  f"""Generate a mitigation strategies for the below vulnerabilities as markdown, give each vulnerability a bolded heading:
{descriptionText}
Generated text starts here:
# Mitigation Strategies
"""

input_ids = tokenizer(input_text, return_tensors="pt").to("cuda").input_ids
outputs = model.generate(input_ids, max_new_tokens=1000)
result = tokenizer.decode(outputs[0])
startIndex = result.find(separator) + len(separator)
outputFile.write(result[startIndex:])
print(result)
outputFile.close()