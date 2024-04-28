import nmap

from sys import stderr
from datetime import datetime

from models import db, Scan
from app import create_app, env

from sys import argv
from pprint import pprint
from json import dump

app = create_app()

def test_scanner(message):
    return "Pong" if message == "Ping" else "Failed"

def scanner(ip: str):
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
            return scan_.id
    except Exception as e:
        with app.app_context():
            scan_.status = 'failed'
            db.session.add(scan_)
            db.session.commit()
        print(f"Error scanning {ip}: {e}", file=stderr)
        return None

def simple_scan(ip):
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