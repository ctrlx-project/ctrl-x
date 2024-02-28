"""
This app runs as a separate process and is responsible for scanning the network. It can be used to dispatch a scan job
from the main app. It shares the codebase with main app.

How to use:
    /POST: Dispatch a scan job
        Form Params:
            - ip: IP of the scan job to be dispatched
        This also changes the status of the scan job (status) to 'running' and sets the start time in the database.
"""

import ipaddress
import nmap
import concurrent.futures
import threading

from sys import stderr
from flask import request
from utils import success_resp, error_resp
from datetime import datetime
from dns import resolver
from dataclasses import dataclass
from time import sleep
from re import match

from models import db, Scan, Setting
from app import create_app


@dataclass
class Env:
    nmap_scan_args = "-Pn -sS -sV -A -T5 --script=default,discovery,vuln"
    nameserver = "1.1.1.1"
    resolver = resolver.Resolver()

    stop_event = threading.Event()

    def update(self):
        with app.app_context():
            self.nmap_scan_args = Setting.query.get('nmap_scan_args').first().value
            self.resolver.nameservers = [Setting.query.get('nameserver').first().value, '8.8.8.8']

    def __update(self):
        while not self.stop_event.is_set():
            try:
                self.update()
            except Exception as e:
                print(f"Error updating settings: {e}", file=stderr)
            finally:
                sleep(3)

    def start(self):
        threading.Thread(target=self.__update, daemon=True).start()

    def stop(self):
        self.stop_event.set()


env = Env()


def nm_scan(ip: str):
    nm = nmap.PortScanner()
    scan = Scan(ip=ipaddress.ip_network(ip, strict=False), status='running', start_time=datetime.now())
    db.session.add(scan)
    db.session.commit()
    nm.scan(ip, arguments=env.nmap_scan_args)
    scan_data = nm.analyse_nmap_xml_scan()
    scan.scan_data = scan_data
    scan.status = 'complete'
    scan.end_time = datetime.now()
    db.session.add(scan)
    db.session.commit()


def scan_job(subnet_ip: str):
    if not match(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', subnet_ip):
        subnet_ip = env.resolver.query(subnet_ip, 'A')

    ip_list = [str(ip) for ip in ipaddress.IPv4Network(subnet_ip, strict=False)]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []

        for ip in ip_list:
            futures.append(executor.submit(nm_scan, ip))

        for future in concurrent.futures.as_completed(futures):
            future.result()


if __name__ == "__main__":
    sleep(3)
    app = create_app()
    env.start()


    @app.route('/', methods=['POST'])
    def index():
        ip = request.form.get('ip')
        if not ip:
            return error_resp('IP is required')
        threading.Thread(target=scan_job, args=(ip,)).start()
        return success_resp(f"Scan job for {ip} dispatched at {datetime.now()}")


    app.run(port=8000, debug=True)
