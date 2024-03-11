# pip install accelerate
from transformers import AutoTokenizer, AutoModelForCausalLM
import time
import requests

accessToken = "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"

# """
# {host: {port: {worked: [CVE], not_worked: [CVE]}}}
# """

cveList = ["CVE-2012-0814", "CVE-2008-1657", "CVE-2011-2168", "CVE-2011-4327","CVE-2008-5161","CVE-2010-4478","CVE-2011-5000","CVE-2008-3259","CVE-2010-5107","CVE-2011-1013", "CVE-2010-4754", "CVE-2010-4755"]

def getDescription(cveList: list) -> str:
     descriptions = ""
     for cve in cveList:
          r = requests.get(f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve}")
          try:
               r_dict = r.json()
          except:
               # print(f"Problem for {cve}: ", r.text)
               continue
          vulnerabilities = r_dict.get("vulnerabilities")
          if vulnerabilities and len(vulnerabilities) == 1:
               cve = vulnerabilities[0].get("cve")
               if cve and cve.get("descriptions"):
                    descriptionList = cve.get("descriptions")
                    for description in descriptionList:
                         if description.get("lang") == "en" and description.get("value") is not None:
                              descriptions += description.get("value") + "\n" 
     return descriptions

descriptions = getDescription(cveList)
print(descriptions)

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
outputs = model.generate(input_ids, max_new_tokens=1000)
end = time.time()

print("Generation time: ", end-start)

start = time.time()
for i in range(len(outputs)):
    result = tokenizer.decode(outputs[i])
    print(result)
end = time.time()
print("Output tokenized: ", end -start)