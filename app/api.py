from flask import Blueprint, request, escape, jsonify, render_template
from models import db, Scan, Report, Setting, Exploit
from utils import success_resp, error_resp, validate_scan_job
import requests

from celery.result import AsyncResult
from time import sleep
from app import create_app, env
from flask_login import current_user
from pymetasploit3.msfrpc import MsfRpcClient, MsfAuthError


from tasks import dispatch_scan, test_mq

api = Blueprint('api', __name__, static_folder='static', template_folder='templates')

app = create_app()


@api.route('/')
def _api():
    return success_resp("API is running")



@api.route('/test-scan')
def test_mq():
    # Test scannerd by sending message to it, and then checking the reply
    result = test_mq.delay("Ping")
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
    if current_user.is_authenticated or env.api_key == request.headers.get("X-api-key"):
        # Dispatch scan using block/FQDN. This passes the job to scanner
        ip_block = request.form.get('ip_block')
        ports = request.form.get('ports')
        if not ip_block:
            return error_resp('IP/IP-block/FQDN is required')
        if ip_block := validate_scan_job(ip_block):
            return dispatch_scan(ip_block, ports)
        else:
            return error_resp('Invalid IP/FQDN')
    else:
        return error_resp('Must be logged in to request a new scan.')


@api.route('/scan', methods=['GET'])
def scans():
    login = current_user.is_authenticated
    if current_user.is_authenticated or env.api_key == request.headers.get("X-api-key"):
        # if GET method, return all scans in database
        if request.method == 'GET':
            if ip := request.args.get('ip'):
                request_ip = str(escape(ip))
                result = Scan.query.filter_by(ip = request_ip)
                if result:
                    ret = [scan.info for scan in result]
                    p_list = sorted(ret, key=lambda x: x['start_time'])
                    return render_template("scan.html", scan_list=p_list, login=login)
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
    else:
        return error_resp('Must be authenticated to see scans')

@api.route('/exploit', methods=['GET'])
def exploits():
    login = current_user.is_authenticated
    if current_user.is_authenticated or env.api_key == request.headers.get("X-api-key"):
        # if GET method, return all exploits in database
        if request.method == 'GET':
            if ip := request.args.get('ip'):
                request_ip = str(escape(ip))
                result = Exploit.query.filter_by(ip = request_ip)
                if result:
                    ret = [exploit.info for exploit in result]
                    p_list = sorted(ret, key=lambda x: x['start_time'])
                    return render_template("exploit.html", exploit_list=p_list, login=login)
                else:
                    return error_resp(f"Exploit with ip {request_ip} not found.")
            else:
                result = Exploit.query.all()
                if result:
                    ret = [exploit.info for exploit in result]
                    p_list = sorted(ret, key=lambda x: x['start_time'])
                    return jsonify(p_list)
                else:
                    return error_resp("No exploits yet!")
    else:
        return error_resp('Must be authenticated to see exploits')

@api.route('/report', methods=['GET'])
def reports():
    if current_user.is_authenticated or env.api_key == request.headers.get("X-api-key"):
        # if GET method, return all reports in database
        if request.method == 'GET':
            result = Report.query.all()
            if result:
                ret = [report.info for report in result]
                p_list = sorted(ret, key=lambda x: x['time'])
                return jsonify(p_list)
            else:
                return error_resp("No reports yet!")
    else:
        return error_resp('Must be authenticated to see reports')

@api.route('/shells', methods=['GET'])
def shells():
    if current_user.is_authenticated or env.api_key == request.headers.get("X-api-key"):
        # If GET method, return all shells
        if request.method == 'GET':
            try:
                msf_manager = MsfRpcClient(env.msf_password, ip=env.msf_ip, port=env.msf_port)
                result = msf_manager.sessions.list
            except MsfAuthError:
                return error_resp("MsfRPC server is offline.")
            if result:
                return jsonify(result)
            else:
                return error_resp("No shells yet!")
    else:
        return error_resp('Must be authenticated to see shells')


@api.route('/settings', methods=['GET', 'POST'])
def settings():
    if current_user.is_authenticated or env.api_key == request.headers.get("X-api-key"):
        # if GET request, then return current settings
        if request.method == 'GET':
            settings = Setting.query.all()
            ret = [config.info for config in settings]
            return jsonify(ret)
        # if POST request, then update settings
        if request.method == 'POST':
            command = request.form.get('command')
            dns_val = request.form.get('dns')
            print(dns_val, command)
            if not (command or dns_val):
                return error_resp('Entering a change is required')
            if command:
                command_settings = Setting.query.filter_by(key="nmap_scan_args").first()
                command_settings.value = command
                db.session.add(command_settings)

            if dns_val:
                dns_settings = Setting.query.filter_by(key="nameserver").first()
                dns_settings.value = dns_val
                db.session.add(dns_settings)
            print(dns_val, command)

            db.session.commit()
            return success_resp(f'Successfully changed settings to {command}')

            # if command:
            #     command_setting = Setting.query.all()[0]
            #     if command_setting:
            #         with app.app_context():
            #             command_setting.value = command
            #             db.session.commit()
            #         return success_resp(f'Successfully changed settings to {command}')
            #     else:
            #         return error_resp('Could not find settings, contact administrator.')
            # if dns_val:
            #     dns_setting = Setting.query.all()[1]
            #     if dns_setting:
            #         with app.app_context():
            #             dns_setting.value = dns_val
            #             db.session.commit()
            #         return success_resp(f'Successfully changed settings to {dns_val}')
            #     else:
            #         return error_resp('Could not find settings, contact administrator.')
    else:
        return error_resp('Must be logged in to request a new scan.')


@api.route('/store_report', methods=['POST'])
def store_report():
    if env.api_key != request.headers.get("X-api-key"):
        return error_resp('Not open to public')
    print(request.form)
    report_id = request.form.get("report_id")
    if not report_id:
        return error_resp('Missing report id')
    report_status = request.form.get("status")
    report = Report.query.filter_by(id=report_id).first()
    if report_status is not None and report_status == "complete" and request.form.get("report") is not None:
        report_content = request.form.get("report")
        report.status = "complete"
        report.content = report_content
        db.session.add(report)
        db.session.commit()
        print("Complete")
    else:
        report.status = "failed"
        db.session.add(report)
        db.session.commit()
        print("Failed")
    return success_resp("Success")
