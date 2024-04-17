from flask import Blueprint, request
from models import db, Scan
from utils import success_resp, error_resp, validate_scan_job
from scannerd import scan, test_scannerd
from celery.result import AsyncResult
from time import sleep

api = Blueprint('api', __name__, static_folder='static', template_folder='templates')


@api.route('/')
def _api():
    return success_resp("API is running")


@api.route('/test-scan')
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


@api.route('/scan', methods=['POST'])
def _scan_():
    ip_block = request.form.get('ip_block')
    if not ip_block:
        return error_resp('IP/IP block/FQDN is required')
    if ip_block := validate_scan_job(ip_block):
        scan.delay(ip_block=ip_block)
        return success_resp('Scan job dispatched')
    else:
        return error_resp('Invalid IP/FQDN')
