# pip install accelerate
from transformers import AutoTokenizer, AutoModelForCausalLM
import time
import requests

accessToken = "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"

cveList = ["CVE-2012-0814", "CVE-2008-1657", "CVE-2011-2168", "CVE-2011-4327","CVE-2008-5161","CVE-2010-4478","CVE-2011-5000","CVE-2008-3259","CVE-2010-5107","CVE-2011-1013", "CVE-2010-4754", "CVE-2010-4755"]
descriptions = ""
for cve in cveList:
      r = requests.get(f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve}")
      r_dict = r.json()
      vulnerabilities = r_dict.get("vulnerabilities")
      if vulnerabilities and len(vulnerabilities) == 1:
            cve = vulnerabilities[0].get("cve")
            if cve and cve.get("descriptions"):
                 descriptionList = cve.get("descriptions")
                 for description in descriptionList:
                      if description.get("lang") == "en" and description.get("value") is not None:
                           descriptions += description.get("value") + "\n" 


tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b-it", token=accessToken)
model = AutoModelForCausalLM.from_pretrained("google/gemma-2b-it", device_map="auto", token=accessToken)

    

input_text =  f"""Generate a pentetration testing report for a network. The reprot should contain an executive summary, description of vulnerabilities, and conclusion.
Below are the vulnerabilities of the network:
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