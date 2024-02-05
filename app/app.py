from dataclasses import dataclass
from os import environ

from flask import Flask
from models import db


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
