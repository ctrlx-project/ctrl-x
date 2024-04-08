from flask import Blueprint,request,escape,jsonify
from models import db, Scan
from utils import success_resp, error_resp

api = Blueprint('api', __name__, static_folder='static', template_folder='templates')


@api.route('/')
def _api():
    return success_resp("API is running")

@api.route('/getscans', methods=['GET','POST'])
def get_scans():
    # if GET method, return all scans in database
    if request.method == 'GET':
        result = Scan.query.all()
        if result:
            ret = [scan.info for scan in result]
            return jsonify(ret)
        else:
            return error_resp("No scans yet!")
    # if POST method, return scans with matching IP's
    elif request.method == "POST":
        if ip:=request.form.get('ip'):
            request_ip = str(escape(ip))
            result = Scan.query.filter(Scan.ip==request_ip)
            if result:
                ret = [scan.info for scan in result]
                return jsonify(ret)
            else:
                return error_resp(f"Scans with ip {request_ip} not found.")
        else:
            return error_resp("IP is required for this method to be used.")





