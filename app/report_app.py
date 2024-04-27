from flask import Flask, abort, request, jsonify
from os import environ
from report import generate_report
from multiprocessing import Process
from json import loads
from transformers import AutoTokenizer, AutoModelForCausalLM
import requests

app = Flask(__name__)
api_key = environ.get("api_key")
LOCKED = False
access_token = environ.get("ml_access_token")
server = environ.get("server")

pretrained = "google/gemma-2b-it"
tokenizer = AutoTokenizer.from_pretrained(pretrained, token=access_token)
model = AutoModelForCausalLM.from_pretrained(pretrained, device_map="auto", token=access_token)

@app.route("/genReport", method=["POST"])
def get_report():
    if request.api_key != api_key:
        return abort(401)
    try:
        report_id = request.form.report_id
        exploit_data = loads(request.form.exploit_data)
        report_generation = Process(target=return_report, args=(report_id, exploit_data))
        report_generation.start()
        return {"status":"runnning"}
    except Exception:
        return {"status":"failed"}

def return_report(report_id:int, exploit_data:dict)->None:
    while (LOCKED):
        continue
    LOCKED = True
    result = generate_report(exploit_data, tokenizer, model)
    requests.post(server, data={"report_id":report_id, "report":result})



