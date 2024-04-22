from flask import Blueprint,request,escape,jsonify
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
    # Test scannerd by sending message to it, and then checking the reply
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


@api.route('/scan-new', methods=['POST'])
def _scan_():
    # Dispatch scan using block/FQDN. This passes the job to scannerd
    ip_block = request.form.get('ip_block')
    if not ip_block:
        return error_resp('IP/IP block/FQDN is required')
    if ip_block := validate_scan_job(ip_block):
        scan.delay(ip_block=ip_block)
        return success_resp('Scan job dispatched')
    else:
        return error_resp('Invalid IP/FQDN')

      
@api.route('/scan', methods=['GET'])
def scans():
    # if GET method, return all scans in database
    if request.method == 'GET':
        if ip:=request.args.get('ip'):
            request_ip = str(escape(ip))
            result = Scan.query.filter(Scan.ip==request_ip)
            if result:
                ret = [scan.info for scan in result]
                p_list = sorted(ret, key=lambda x: x['start_time'])
                return jsonify(p_list)
            else:
                return error_resp(f"Scans with ip {request_ip} not found.")
        else:
            result = Scan.query.all()
            if result:
                ret = [scan.info for scan in result]
                p_list = sorted(ret, key=lambda x: x['start_time'])
                return jsonify(p_list)
            else:
                return error_resp("No scans yet!")
