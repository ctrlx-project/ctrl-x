from dataclasses import dataclass
from os import environ

from flask import Flask
from models import db
from flask_migrate import Migrate

from celery import Celery, Task


@dataclass
class Env:
    postgres_url: str = environ.get("POSTGRES_URL", default="postgresql://admin:admin@localhost:5432/ctrl-x")
    scannerd_url: str = environ.get("SCANNERD_URL", default="http://localhost:8000")
    broker_url: str = environ.get("RABBITMQ_URL", default="amqp://admin:admin@localhost:5672")
    result_backend: str = environ.get("POSTGRES_URL", default="db+postgresql://admin:admin@localhost:5432/ctrl-x")
    task_ignore_result: bool = True


env = Env()


def celery_init(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = env.postgres_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = False

    db.init_app(app)

    migrate = Migrate(app, db)

    app.config.from_mapping(
        CELERY=dict(
            broker_url=env.broker_url,
            result_backend=env.result_backend,
            task_ignore_result=env.task_ignore_result,
            broker_connection_retry_on_startup=True,
        ),
    )

    app.config.from_prefixed_env()
    celery_init(app)

    return app
