import ipaddress
import nmap
import concurrent.futures
from sys import argv

from app import create_app
from models import db, Scans

app = create_app()

def nm_scan(ip):
    nm = nmap.PortScanner()
    nm.scan(ip, arguments="-Pn -sS -sV -T4 --script=default,discovery,vuln")
    scan_data = nm.analyse_nmap_xml_scan()
    return scan_data, ip


def save_to_db(data, ip):
    scan = Scans(ip=ip, scan_data=data)
    with app.app_context():
        db.session.add(scan)
        db.session.commit()


def scan_subnet(subnet):
    # If the subnet is a single IP
    if not '/' in subnet:
        res = nm_scan(subnet)
        save_to_db(res[0], res[1])
        return

    ip_list = [str(ip) for ip in ipaddress.IPv4Network(subnet, strict=False)]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for ip in ip_list:
            futures.append(executor.submit(nm_scan, ip))

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            save_to_db(result[0], result[1])


if __name__ == "__main__":
    if len(argv) < 2:
        print("Usage: py scan.py <subnet>; e.g. py scan.py 10.1.0.0/24")
    print("Scanning", argv[1])
    scan_subnet(argv[1])
