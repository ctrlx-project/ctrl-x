from sys import argv
from utils import load_json
from models import db, Parsed, Scan
from datetime import datetime
import json


def get_cve(string: str) -> list:
    """Parses a given string and returns a list of all CVEs included on it.

    Args:
        (dict): Dictionary output from the Nmap scan

    Returns:
        (list): List of CVE's found.
    """
    index = string.find("CVE")
    result = set()
    while index != -1:
        final_index = -1
        for i in range(index, len(string)):
            if string[i] == "\n" or string[i] == "\t":
                final_index = i
                break
        result.add(string[index:final_index])
        string = string[final_index:]
        index = string.find("CVE")
    result = list(result)
    result.sort()
    return result


def parse_scan_result_(scan_result: dict) -> dict:
    """ Parse a single scan dictionary and extract useful information.
    The return result should be a dictionary contain the state of the host, 
    transport layer protocols that find open ports, 
    information regarding open ports, and vulnerability 
    If the host is not up, Empty dictionary is returned.

    Args:
        (dict): Dictionary output from the Nmap scan

    Returns:
        (dict): Parsed scan with useful information for metasploit
        The structure of the output dictionary is:
        {ip:{
            "state": "up"/"down", 
            "ports": {
                port_number : {
                    "transport_protocol": transport protocol used to connect to the port
                    "name": portName,
                    "service": service running on that port
                    "vulner": set(CVE_numbers)
                }
            } 
        }}
    """
    result = {}
    scan = scan_result.get("scan")
    if scan is None:
        return {}
    if len(scan.keys()) < 1:
        return {}
    for network in scan.keys():
        network_result = scan.get(network)
        state = network_result.get("status", {}).get("state")
        if state is None:
            return {}
        result[network] = {"state": state}
        if state != "up":
            return {}
        fields = ["tcp", "udp"]
        network_keys = network_result.keys()
        result[network]["ports"] = {}
        for field in fields:
            if field in network_keys:
                current = network_result.get(field)
                ports = []
                if current is not None:
                    ports = current.keys()
                for port in ports:
                    port_result = current.get(port)
                    if port_result.get("state") == "open":
                        result[network]["ports"][port] = {"transport_protocol": field}
                        name = port_result.get("name")
                        if name:
                            result[network]["ports"][port]["name"] = name
                        product = port_result.get("product").strip()
                        version = port_result.get("version").strip()
                        if product:
                            service = f'{product} {version}'.strip()
                            result[network]["ports"][port]["service"] = service
                        vulner = port_result.get("script", {}).get("vulners")
                        if vulner and isinstance(vulner, str):
                            result[network]["ports"][port]["vulner"] = get_cve(vulner)
    return result


def parse_from_json(file):
    """ Parse a single JSON scan file and extract useful informations.

    Args:
        (str): The path of the scan file.

    Returns:
        (dict): Parsed scan with useful information for metasploits.
    """
    dictionary = load_json(file)
    return parse_scan_result_(dictionary)


def parse_scan(scan_id: str):
    """ 
    Parse a single scan job and extract useful information
    Args:
        scan_id: The id of the scan job to be parsed
    Returns:
        Parsed scan id, scan id
    """
    if scan_id:
        # Gets the Scan from the database
        saved_scan = Scan.query.filter_by(id=scan_id).first()

        # Creates the Parsed object in the database
        loaded_scan = json.loads(saved_scan.scan_data)
        ip = next(iter(loaded_scan["scan"]))

        parsed_scan = Parsed(ip=ip, start_time=datetime.now(), status='running')
        db.session.add(parsed_scan)
        db.session.commit()

        # Updates the Parsed object in the database
        parsed_scan.parsed_data = parse_scan_result_(loaded_scan)
        parsed_scan.status = 'complete'
        parsed_scan.end_time = datetime.now()
        db.session.add(parsed_scan)
        db.session.commit()

        return parsed_scan.id, scan_id

    return None, None


def main():
    result = parse_from_json(argv[1])
    print(result)


if __name__ == "__main__":
    if len(argv) < 2:
        print("Usage: py parse_scan.py <file>; e.g. py scan.py seed/10.1.0.1.json")
        exit(1)
    main()
