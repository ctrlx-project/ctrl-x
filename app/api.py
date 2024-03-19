from flask import Blueprint,request,escape,jsonify
from models import db, Scan
from utils import success_resp, error_resp

api = Blueprint('api', __name__, static_folder='static', template_folder='templates')


@api.route('/')
def _api():
    return success_resp("API is running")

@api.route('/getscans', methods=['GET'])
def get_scans():
    fields = ['id', 'ip', 'scan_data', 'start_time', 'end_time', 'status']
    num_fields = len(fields)
    # if GET method, return all scans in Database
    if request.method == 'GET':
        if query := Scan.query.all():
            ret = []
            for scan in query:
                scans = [scan.id, scan.ip, scan.scan_data, scan.start_time, scan.end_time, scan.status]
                scan_dict = {fields[idx]:scans[idx] for idx in range(num_fields)}
                ret.append(scan_dict)
            return ret
        else:
            return error_resp("No scans yet!")
        
    # if POST method, return scans with matching IP's
    elif request.method == "POST":
        ...

