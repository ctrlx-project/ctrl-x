"""
This app runs as a separate process and is responsible for scanning the network. It can be used to dispatch a scan job
from the main app. It shares the codebase with main app.

How to use:
    Dispatch a scan job from main app:
        Worker Params:
            - ip_block: IP/FQDN of the scan job to be dispatched
        This also changes the status of the scan job (status) to 'running' and sets the start time in the database.
        When it is done, it updates the status to 'complete' and sets the end time.
"""

import nmap
import concurrent.futures

from sys import stderr
from datetime import datetime
from typing import NoReturn as Never

from models import db, Scan
from app import env, create_app
from utils import resolve_ip_block
from celery import shared_task
from sys import argv
from pprint import pprint
from json import dump

@shared_task(ignore_result=False, name='scannerd_test')
def test_scannerd(message):
    return "Pong" if message == "Ping" else "Failed"

def nm_scan(ip: str):
    with app.app_context():
        scan_ = Scan(ip=ip)
        scan_.status = 'running'
        db.session.add(scan_)
        db.session.commit()

    try:
        scan_data = simple_scan(ip)
        with app.app_context():
            scan_.scan_data = scan_data
            scan_.status = 'complete'
            scan_.end_time = datetime.now()
            db.session.add(scan_)
            db.session.commit()
    except Exception as e:
        with app.app_context():
            scan_.status = 'failed'
            db.session.add(scan_)
            db.session.commit()
        print(f"Error scanning {ip}: {e}", file=stderr)


def scan_job(ip_block: list[str]):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []

        for ip in ip_block:
            futures.append(executor.submit(nm_scan, ip))

        for future in concurrent.futures.as_completed(futures):
            future.result()


@shared_task(ignore_result=True, name='scannerd_scan', autoretry_for=(Exception,), retry_backoff=True,
             retry_jitter=True, retry_kwargs={'max_retries': 3})
def scan(ip_block: str) -> Never:
    """
    Takes in ip in the format a.b.c.d/CIDR, a.b.c.d, or domain name; or id of scheduled scan job
    Args:
        ip_block:  IP/FQDN of the scan job to be dispatched
    Returns:
        dict: Response message
    """
    if ip_block:
        scan_job(resolve_ip_block(ip_block))

def simple_scan(ip) -> Never:
    """
    Takes in ip in the format a.b.c.d/CIDR, a.b.c.d, or domain name; or id of scheduled scan job
    Args:
        ip:  IP of the scan job to be dispatched
    Returns:
        dict: Scan data
    """
    nm = nmap.PortScanner()
    nm.scan(ip, arguments=env.nmap_scan_args)
    return nm.analyse_nmap_xml_scan()

def main():
    print(f"Scanning IP {argv[1]}")
    scan_data = simple_scan(argv[1])
    print(f"Scan results:")
    pprint(scan_data)
    if len(argv) > 2:
        print(f"Saving Scan on {argv[2]}")
        with open(argv[2], 'w') as fp:
            dump(scan_data, fp)

if __name__ == "__main__":
    if len(argv) < 2:
        print("Usage: py scannerd.py [target_ip] [output_file]")
        print("\te.g. py scannerd.py 10.10.0.13  seed/nmap/10.10.0.13.json")
        exit(1)
    main()
else:
    app = create_app()
    celery_app = app.extensions["celery"]
    celery_app.set_default()
    env.app = app
