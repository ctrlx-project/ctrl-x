from dataclasses import dataclass
from os import environ
from sys import stderr

from flask import Flask
from models import db, Setting, User
from flask_migrate import Migrate
from flask_login import LoginManager

from celery import Celery, Task

from dns import resolver
import threading
from time import sleep
from datetime import timedelta


@dataclass
class Env:
    postgres_url: str = environ.get("POSTGRES_URL", default="postgresql://admin:admin@localhost:5432/ctrl-x")
    scannerd_url: str = environ.get("SCANNERD_URL", default="http://localhost:8000")
    broker_url: str = environ.get("RABBITMQ_URL", default="amqp://admin:admin@localhost:5672")
    result_backend: str = environ.get("POSTGRES_URL", default="db+postgresql://admin:admin@localhost:5432/ctrl-x")
    secret_key:str = environ.get("SECRET_KEY", default="dingdongbingbongbangdangpfchans")

    app = None

    # For scannerd
    task_ignore_result: bool = True
    nmap_scan_args = "-Pn -sS -sV -A -T5 --script=default,discovery,vuln"
    resolver = resolver.Resolver()
    resolver.nameservers = ['1.1.1.1', '8.8.8.8']

    stop_event = threading.Event()

    def update(self):  # Updates setting values from the database
        with self.app.app_context():
            self.nmap_scan_args = Setting.query.filter_by(key='nmap_scan_args').first().value or self.nmap_scan_args
            self.resolver.nameservers = [Setting.query.filter_by(key='nameserver').first().value,
                                         '8.8.8.8'] or self.resolver.nameservers

    def __update__(self):  # Update settings from the database every 3 seconds
        while not self.stop_event.is_set():
            try:
                self.update()
            except Exception as e:
                print(f"Error updating settings: {e}", file=stderr)
            finally:
                sleep(3)

    def __post_init__(self):  # Start the update thread after class initialization
        threading.Thread(target=self.__update__, daemon=True).start()


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
    app.config['SECRET_KEY'] = env.secret_key
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

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

    login_manager = LoginManager()
    login_manager.login_view = "underground.underground_home"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    return app
