import threading

from flask import request
from sys import argv
from datetime import datetime
from utils import success_resp, error_resp, load_json
from app import create_app

app = create_app()



def get_cve(string:str)->set:
    """Parses a given string and returns a list of all CVEs included on it.

    Args:
        (dict): Dictionary output from the Nmap scan

    Returns:
        (dict): Parsed scan with useful information for metasploit
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
    return result


def parse_scan(scan_result:dict)->dict:
    """ Parse a single scan dictionary and extract useful informations.
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
    if (len(scan.keys()) < 1):
        return {}
    for network in scan.keys():
        network_result = scan.get(network)
        state = network_result.get("status",{}).get("state")
        if state is None:
            return {}
        result[network] = {"state": state}
        if (state != "up"):
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
                        vulner = port_result.get("script",{}).get("vulners")
                        if vulner and isinstance(vulner, str):
                            result[network]["ports"][port]["vulner"] = list(get_cve(vulner))
    return result


@app.route('/', methods=['POST'])
def index():
    scan_id = request.form.get('sid')
    scan = request.form.get('scan.json')
    if scan_id:
        # todo: retrieve parsed scan from the database
        json_scan = {}
        scan = load_json(json_scan)
    else:
        return error_resp('Please provide a scan to be parsed.')
    threading.Thread(target=parse_scan, args=scan).start()
    return success_resp(f"Parsing job for {scan_id} dispatched at {datetime.now()}")

if __name__ == "__main__":
    if len(argv) == 1:
        app.run(port=10000, debug=True)
    elif len(argv) != 2:
        print("Usage: py parse_scan.py [file_path]")
        print("\te.g. py scan.py seed/10.1.0.1.json")
        exit(1)
    loaded_scan = load_json(argv[1])
    parsed_scan = parse_scan(loaded_scan)
    print(parsed_scan)
