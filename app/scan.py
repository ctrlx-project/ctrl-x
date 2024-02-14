import ipaddress
import nmap
import concurrent.futures
import json
from sys import stderr
from os import path
from pathlib import Path
from datetime import datetime

from app import create_app
from models import db, Scans

from utils import pretty_print

# Temporary argparse code - will be replaced by flask

import argparse

app = create_app()
parser = argparse.ArgumentParser(
                    prog='ctrl-x-scan',
                    description='Scans a subnet')
parser.add_argument('subnet', help='Subnet to be scanned.')
parser.add_argument('-D', '--disable_db', action='store_true', help='Does not store result on database.')
parser.add_argument('-O', '--output_dir', help='Sets the output directory.')

# End of temporary code

DATETIME_FORMAT = '"%Y-%m-%d_%H-%M-%S"'

def nm_scan(ip: str) -> tuple:
    """Scans the given IP address using Nmap.

    Args:
      ip (str): The IP address of the scan.

    Returns:
        (tuple): The IP address and the result of its scan.
    """
    nm = nmap.PortScanner()
    nm.scan(ip, arguments='-Pn -sS -sV -A -T5 --script=default,discovery,vuln')
    scan_data = nm.analyse_nmap_xml_scan()
    return ip, scan_data


def save_to_db(ip: str, data: dict):
    """Saves a scan to the database.

    Args:
      ip (str): The IP address of the scan.
      data (dict): The data of the scan.
    """
    scan = Scans(ip=ip, scan_data=data)
    with app.app_context():
        db.session.add(scan)
        db.session.commit()

def save_as_json(ip: str, data: str, directory: str):
    """Saves a scan as a json file.

    Args:
      ip (str): The IP address of the scan.
      data (str): The data of the scan.
    """
    file_name = f'{ip}_{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.json'
    directory = Path(directory)
    directory.mkdir(exist_ok=True)
    file_path = directory / file_name
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def scan_subnet(subnet: str) -> dict:
    """Scans a subnet with Nmap and returns the result.

    Args:
      subnet (str): A TurbiniaTask object

    Returns:
      (dict) A dictionary of results for each ip address scanned.
    """
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

if __name__ == "__main__":
    args = parser.parse_args()

    if not args.subnet:
        pretty_print("--- Usage: make scan <subnet>; e.g. make scan 10.1.0.0/24", file=stderr)
        exit(1)

    pretty_print(f"Scanning {args.subnet}")

    scan_results = scan_subnet(args.subnet)

    for scan_ip, scan_result in scan_results.items():
        if not args.disable_db:
            save_to_db(scan_ip, scan_result)
        if args.output_dir:
            save_as_json(scan_ip, scan_result, args.output_dir)
        save_as_json(scan_ip,scan_result, "data")
    
     
