import nmap

from sys import stderr
from datetime import datetime

from models import db, Scan
from app import create_app, env

app = create_app()


def test_scanner(message):
    return "Pong" if message == "Ping" else "Failed"


def scanner(ip: str):
    nm = nmap.PortScanner()
    with app.app_context():
        scan_ = Scan(ip=ip)
        scan_.status = 'running'
        db.session.add(scan_)
        db.session.commit()

    try:
        nm.scan(ip, arguments=env.nmap_scan_args)
        scan_data = nm.analyse_nmap_xml_scan()
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
