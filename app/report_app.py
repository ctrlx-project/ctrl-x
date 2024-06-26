from flask import Flask, abort, request
from os import environ
import torch.multiprocessing as mp
from json import loads
from transformers import AutoTokenizer, AutoModelForCausalLM
import requests
from time import sleep
from dotenv import load_dotenv

from report import generate_report

load_dotenv()
app = Flask(__name__)
api_key = environ.get("api_key")
if api_key is None:
    api_key = "dingdongbingbongbangdangpfchans"
access_token = environ.get("ml_access_token")
if access_token is None:
    access_token = "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"
server = environ.get("server")
if server is None:
    server = "https://ctrl.onosiris.io/api/store_report"
environ["LOCKED"] = "False"
try:
   mp.set_start_method('spawn', force=True)
except RuntimeError:
   pass

pretrained = "google/gemma-2b-it"
tokenizer = AutoTokenizer.from_pretrained(pretrained, token=access_token)
model = AutoModelForCausalLM.from_pretrained(pretrained, device_map="auto", token=access_token)

@app.route("/gen_report", methods=["POST"])
def get_report():
    if request.headers.get("X-api-key") != api_key:
        print(request.headers)
        return abort(401)
    try:
        report_id = request.form.get("report_id")
        exploit_data = loads(request.form.get("exploit_data"))
        report_generation = mp.Process(target=return_report, args=(report_id, exploit_data))
        report_generation.start()
        return {"status":"runnning"}
    except Exception as e:
        return {"status":"failed", "error":str(e)}

def return_report(report_id:int, exploit_data:dict)->None:
    while (environ.get("LOCKED") == "True"):
        sleep(3)
    environ["LOCKED"] = "True"
    headers = {"X-api-key":api_key}
    try:
        result = generate_report(exploit_data, tokenizer, model)
        requests.post(server, data={"report_id":report_id, "report":result, "status":"complete"}, headers=headers)
    except:
        requests.post(server, data={"report_id":report_id, "status":"failed"}, headers=headers)
    finally:
        environ["LOCKED"] = "False"



if __name__ == '__main__':
    app.run(port=8000)