from app import create_app
from utils import resolve_ip_block, success_resp
from celery import shared_task, chain
import requests
from json import dumps
from time import sleep

from scanner import test_scanner, scanner
from parse_scan import parse_scan
from exploit import exploit
from models import Report, Scan, Exploit, db


app = create_app()
celery_app = app.extensions["celery"]
celery_app.set_default()


@shared_task(ignore_result=False, name='mq_test')
def test_mq(message):
    return test_scanner(message)


@shared_task(ignore_result=False, name='scan')
def scan_job(ip: str, ports: str=''):
    """
    Scans a single IP address
    Returns: scan_id
    """
    return scanner(ip, ports)


@shared_task(ignore_result=False, name='parse_scan')
def parse_scan_job(scan_id: str):
    """
    Parses the scan job
    Returns parsed_scan_id, scan_id
    """
    return parse_scan(scan_id)


@shared_task(ignore_result=False, name='exploit')
def exploit_job(argv):
    """
    Try to exploit using the parsed scan data
    Returns: exploit_id, scan_id
    """
    parsed_id, scan_id = argv
    return exploit(parsed_id, scan_id)


@shared_task(ignore_result=False, name='report')
def report_job(argv):
    """
    Generate a report using the parsed scan data
    Returns: Bool
    """
    exploit_id, scan_id = argv
    return report(exploit_id, scan_id)


def dispatch_scan(ip_block: str, ports: str=''):
    """
    Takes in ip in the format a.b.c.d/CIDR, a.b.c.d, or domain name
    Args:
        ip_block:  IP/FQDN of the scan job to be dispatched
    Returns:
        dict: Response message
    """

    ip_list = resolve_ip_block(ip_block)
    for ip in ip_list:
        chain(scan_job.s(ip, ports), parse_scan_job.s(), exploit_job.s(), report_job.s()).delay()

    return success_resp(f'{len(ip_list)} scan job(s) dispatched.')

def report(exploit_id:int, scan_id:int) -> bool:
    exploit = Exploit.query.filter_by(id=exploit_id).first()
    scan = Scan.query.filter_by(id=scan_id).first()
    newReport = Report(ip=scan.ip, scan_id=scan, status="running")
    db.session.add(newReport)
    db.session.commit()
    payload = {"api_key":env.api_key, "report_id":newReport.id, "exploit_data": dumps(exploit.exploit_data)}
    r = requests.post("llm-api.onosiris.io/gen_report", data=payload)
    if r.status != 200 or r.json().get("status") != "running":
        newReport.status = "failed"
        return False
    while newReport.status == "running":
        sleep(3)
    return newReport.status == "complete"
