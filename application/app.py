from dataclasses import dataclass
from os import environ

from flask import Flask
from models import db
from flask_migrate import Migrate


@dataclass
class Env:
    postgres_url: str = environ.get("POSTGRES_URL", default="postgresql://admin:admin@localhost:5432/ctrl-x")
    scannerd_url: str = environ.get("SCANNERD_URL", default="http://localhost:8000")


env = Env()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = env.postgres_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = False

    db.init_app(app)

    migrate = Migrate(app, db)

    return app
