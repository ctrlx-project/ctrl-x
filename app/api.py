from flask import Blueprint,request,escape,jsonify
from models import db, Scan
from utils import success_resp, error_resp

api = Blueprint('api', __name__, static_folder='static', template_folder='templates')


@api.route('/')
def _api():
    return success_resp("API is running")

@api.route('/getscans', methods=['GET'])
def get_scans():

    # Function to parse result object and return a list of python dictionaries
    def parse_query(query, fields) -> list:
        num_fields = len(fields)
        ret = []
        for scan in query:
            scans = [scan.id, scan.ip, scan.scan_data, scan.start_time, scan.end_time, scan.status]
            scan_dict = {fields[idx]:scans[idx] for idx in range(num_fields)}
            ret.append(scan_dict)
        return ret
    
    fields = ('id', 'ip', 'scan_data', 'start_time', 'end_time', 'status')
    # if GET method, return all scans in database
    if request.method == 'GET':
        stmt = db.select(Scan)
        if db.session.execute(stmt).first:
            result = db.session.execute(stmt).scalars().all()
            return parse_query(result, fields)
        else:
            return error_resp("No scans yet!")
    # if POST method, return scans with matching IP's
    elif request.method == "POST":
        if request_ip := str(escape(request.form.ip)):
            stmt = db.select(Scan).where(Scan.ip==request_ip)
            if db.session.execute(stmt).first():
                result = db.session.execute(stmt).scalars().all()
                return parse_query(result,fields)
            else:
                return error_resp(f"Scans with ip {request_ip} not found.")
        else:
            return error_resp(f"IP is required for a POST request to this endpoint.")






