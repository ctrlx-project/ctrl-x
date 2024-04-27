from app import env, create_app
from utils import resolve_ip_block
from celery import shared_task, chain

from scanner import test_scanner, scanner
from parse_scan import parse_scan
from exploit import exploit

try:
    from report import report
except Exception:
    skip_report = True
    print("######################################################")
    print("### LLM modules not found. Skipping report generation.")
    print("######################################################")

app = create_app()
celery_app = app.extensions["celery"]
celery_app.set_default()


@shared_task(ignore_result=False, name='mq_test')
def test_mq(message):
    return test_scanner(message)


@shared_task(ignore_result=False, name='scan')
def scan_job(ip: str):
    """
    Scans a single IP address
    Returns: scan_id
    """
    return scanner(ip)


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


def dispatch_scan(ip_block: str):
    """
    Takes in ip in the format a.b.c.d/CIDR, a.b.c.d, or domain name
    Args:
        ip_block:  IP/FQDN of the scan job to be dispatched
    Returns:
        dict: Response message
    """

    ip_list = resolve_ip_block(ip_block)
    for ip in ip_list:
        if skip_report:
            chain(scan_job.s(ip), parse_scan_job.s(), exploit_job.s()).delay()
        else:
            print("Skipping report generation")
            chain(scan_job.s(ip), parse_scan_job.s(), exploit_job.s(), report_job.s()).delay()

    return {
        'status': 'success',
        'message': f'{len(ip_list)} scan jobs dispatched.'
    }
