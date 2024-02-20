from dataclasses import dataclass
from os import environ

from flask import Flask, render_template, url_for, request, redirect
from models import db
import json


@dataclass
class Env:
    postgres_url: str = environ.get("POSTGRES_URL", default="postgresql://admin:admin@localhost:5432/ctrl-x")


env = Env()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = env.postgres_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = False

    db.init_app(app)

    return app

app = create_app()

@app.route("/json", methods=["GET"])
def send_data():
    fs = open('./seed/10.1.0.1.json','r')
    json_dump = fs.read()
    fs.close()
    json_data = json.loads(json_dump)
    return json_data

@app.route("/",methods=["GET"])
def homepage():
    return render_template("front_page.html")