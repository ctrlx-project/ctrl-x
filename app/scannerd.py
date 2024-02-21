import ipaddress
import nmap
import concurrent.futures
import socket

from sys import stderr

from models import db, Scan, ScanJob
from app import create_app

from flask import request, jsonify
from utils import success_resp, error_resp
from threading import Thread


def nm_scan(ip: str) -> tuple[str, dict]:
    nm = nmap.PortScanner()
    nm.scan(ip, arguments='-Pn -sS -sV -A -T5 --script=default,discovery,vuln')
    scan_data = nm.analyse_nmap_xml_scan()
    return ip, scan_data


def scan_subnet(subnet: str) -> dict:
    results = {}

    if '/' not in subnet:
        subnet += '/32'
    ip_list = [str(ip) for ip in ipaddress.IPv4Network(subnet, strict=False)]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []

        for ip in ip_list:
            futures.append(executor.submit(nm_scan, ip))

        for future in concurrent.futures.as_completed(futures):
            result = future.result()

            results[result[0]] = result[1]

    return results


def scan_domain(domain):
    address = socket.gethostbyname(domain)
    scan_subnet(address)


def dispatch_scan_job(ip: str):
    try:
        job = ScanJob(ip=ip, status='running')
        db.session.add(job)
        db.session.commit()

        scan_data = scan_subnet(ip)
        scan = Scan(ip=ip, scan_data=scan_data)

        job.status = 'complete'
        job.end_time = db.func.now()

        db.session.add_all([scan, job])
        db.session.commit()

    except Exception as e:
        print(f"Error: {e}", file=stderr)


if __name__ == "__main__":
    app = create_app()


    @app.route('/', methods=['GET', 'POST'])
    def dispatch():
        ip = request.form.get('ip', request.args.get('ip'))

        if request.method == 'POST':
            if not ip:
                return error_resp('IP is required')
            Thread(target=dispatch_scan_job, args=(ip,)).start()
            return success_resp('OK')

        elif request.method == 'GET':
            if ip:
                job = ScanJob.query.filter_by(ip=ip)
                return jsonify(job.info if job else {})
            return jsonify(list(map(lambda j: j.info, ScanJob.query.all())))


    app.run(port=8000, debug=True)
