"""
This app runs as a separate process and is responsible for scanning the network. It can be used to dispatch a scan job
from the main app. It shares the codebase with main app.

How to use:
    Dispatch a scan job from main app:
        Worker Params:
            - ip: IP/FQDN of the scan job to be dispatched
        This also changes the status of the scan job (status) to 'running' and sets the start time in the database.
        When it is done, it updates the status to 'finished' and sets the end time.
"""

import nmap
import concurrent.futures
import threading

from sys import stderr
from datetime import datetime
from dns import resolver
from dataclasses import dataclass
from time import sleep
from ipaddress import IPv4Network, AddressValueError

from models import db, Scan, Setting
from app import create_app
from utils import success_resp, error_resp
from celery import shared_task

app = create_app()
celery_app = app.extensions["celery"]
celery_app.set_default()

env.app = app

@shared_task(ignore_result=False, name='scannerd.test')
def test_scannerd(message):
    return "Pong" if message == "Ping" else "Failed"


@dataclass
class Env:
    nmap_scan_args = "-Pn -sS -sV -A -T5 --script=default,discovery,vuln"
    resolver = resolver.Resolver()
    resolver.nameservers = ['1.1.1.1', '8.8.8.8']

    stop_event = threading.Event()

    def update(self):
        with app.app_context():
            self.nmap_scan_args = Setting.query.filter_by(key='nmap_scan_args').first().value or self.nmap_scan_args
            self.resolver.nameservers = [Setting.query.filter_by(key='nameserver').first().value,
                                         '8.8.8.8'] or self.resolver.nameservers

    def __update__(self):
        while not self.stop_event.is_set():
            try:
                self.update()
            except Exception as e:
                print(f"Error updating settings: {e}", file=stderr)
            finally:
                sleep(3)

    def __post_init__(self):
        threading.Thread(target=self.__update__, daemon=True).start()


env = Env()


def nm_scan(ip: str):
    nm = nmap.PortScanner()
    scan_ = Scan(ip=ip, status='running')
    db.session.add(scan_)
    db.session.commit()

    try:
        nm.scan(ip, arguments=env.nmap_scan_args)
        scan_data = nm.analyse_nmap_xml_scan()
        scan_.update(dict(scan_data=scan_data, status='complete', end_time=datetime.now()))
    except Exception as e:
        scan_.status = 'failed'
        print(f"Error scanning {ip}: {e}", file=stderr)

    finally:
        db.session.add(scan_)
        db.session.commit()


def scan_job(ip_block: list[str]):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []

        for ip in ip_block:
            futures.append(executor.submit(nm_scan, ip))

        for future in concurrent.futures.as_completed(futures):
            future.result()


@shared_task(ignore_result=False, bind=True, name='scannerd.scan')
def scan(raw_input: str):
    # takes in domain name, or ip in the format a.b.c.d/CIDR
    ip_block = raw_input
    if ip_block is None:
        return error_resp('IP/FQDN is required')

    try:
        ip_block = IPv4Network(ip_block, strict=False)  # will raise AddressValueError if not a valid IP
    except AddressValueError:  # if not a valid IP, try to resolve it
        ip_block = env.resolver.query(ip_block, 'A')[0].to_text()
    except resolver.NXDOMAIN:
        return error_resp('Invalid IP or NXDOMAIN')

    scan_job(ip_block)
    return success_resp(f"Scan job for {raw_input} dispatched at {datetime.now()}")


if __name__ == '__main__':
    pass
