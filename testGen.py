# pip install accelerate
from transformers import AutoTokenizer, AutoModelForCausalLM
import time
import requests

accessToken = "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"

# """
# {host: {port: {worked: [CVE], not_worked: [CVE]}}}
# """

cveList = ["CVE-2012-0814", "CVE-2008-1657", "CVE-2011-2168", "CVE-2011-4327","CVE-2008-5161","CVE-2010-4478","CVE-2011-5000","CVE-2008-3259","CVE-2010-5107","CVE-2011-1013", "CVE-2010-4754", "CVE-2010-4755"]

# Can also get CVSS score
def getDescription(cveList: list) -> str:
     descriptions = ""
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
               if cveData:
                    withDescription = False
                    if cveData.get("descriptions"):
                         descriptionList = cveData.get("descriptions")
                         for description in descriptionList:
                              if description.get("lang") == "en" and description.get("value") is not None:
                                   if len(descriptions) > 0:
                                        descriptions += "\n"
                                   descriptions += description.get("value") 
                                   withDescription = True
                    if cveData.get("metrics"):
                         metric = cveData.get("metrics")
                         if len(metric.keys()) > 0:
                              cvssMetric = metric.get(list(metric.keys())[0])
                              if len(cvssMetric) > 0:
                                   cvssData = cvssMetric[0].get("cvssData")
                                   if cvssData and cvssData.get("vectorString") and cvssData.get("baseScore"):
                                        CVSS.append([cve, cvssData.get("baseScore"), cvssData.get("vectorString")])          
                                        if withDescription:
                                             descriptions += f" CVSS score is {cvssData.get('baseScore')}"
     return descriptions, CVSS

# print("Length of CVE: ", len(cveList))
# descriptions, CVSS = getDescription(cveList)
# print(CVSS)
# print("Length of CVSS: ", len(CVSS))
# print(descriptions)

pretrained = "openchat/openchat_3.5"
# pretrained = "google/gemma-2b-it"
tokenizer = AutoTokenizer.from_pretrained(pretrained, token=accessToken)
model = AutoModelForCausalLM.from_pretrained(pretrained, device_map="sequential", token=accessToken)

# input_text =  f"""Generate a mitigation strategies for the below vulnerabilities:
# {descriptions}
# """

# input_text =  f"""Generate the potential impact for the below vulnerabilities:
# {descriptions}
# """

input_text =  f"""Generate the executive summary of the penetration testing report for a network that has the below vulnerabilities:
{descriptions}
"""

start = time.time()
input_ids = tokenizer(input_text, return_tensors="pt").to("cuda").input_ids
end = time.time()
print("Input tokenized: ", end -start)

start = time.time()
print("Start model generation")
outputs = model.generate(input_ids, max_new_tokens=1000)
end = time.time()

print("Generation time: ", end-start)

start = time.time()
for i in range(len(outputs)):
    result = tokenizer.decode(outputs[i])
    print(result)
end = time.time()
print("Output tokenized: ", end -start)