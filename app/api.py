from flask import Blueprint
from models import db, Scan
from utils import success_resp, error_resp
from scannerd import scan, test_scannerd
from celery.result import AsyncResult
from time import sleep

api = Blueprint('api', __name__, static_folder='static', template_folder='templates')


@api.route('/')
def _api():
    return success_resp("API is running")


@api.route('/test_mq')
def test_mq():
    result = test_scannerd.delay("Ping")
    sleep(1)
    result = AsyncResult(result.id)
    return {
        "id": result.id,
        "ready": result.ready(),
        "success": result.successful(),
        "message": "Ping",
        "reply": result.result if result.ready() else None
    }
