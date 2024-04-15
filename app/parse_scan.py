import json
from sys import argv
from typing import Any


def loadJSON(file_path: str) -> dict | list:
    """Loads the file located at the given path.

    Args:
        (str): Path of the file to be loaded

    Returns:
        (dict | list): Object with contents of the loaded JSON file
    """
    try:
        with open(file_path, "r") as json_file: 
            return json.load(json_file)
    except FileNotFoundError:
        print(f"File {file_path} does not exist")
        exit(1)

def get_CVE(string:str)->set:
    """Parses a given string and returns a list of all CVEs included on it.

    Args:
        (dict): Dictionary output from the Nmap scan

    Returns:
        (dict): Parsed scan with useful information for metasploit
    """
    index = string.find("CVE")
    result = set()
    while index != -1:
        finalIndex = -1
        for i in range(index, len(string)):
            if string[i] == "\n" or string[i] == "\t":
                finalIndex = i
                break
        result.add(string[index:finalIndex])
        string = string[finalIndex:]
        index = string.find("CVE")
    return list(result)


def parse_scan(scanResult:dict)->dict:
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
    scan = scanResult.get("scan")
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
                        if vulner and type(vulner) == str:
                            result[network]["ports"][port]["vulner"] = list(get_CVE(vulner))     
    return result


def parse_from_JSON(file):
    dict = loadJSON(file)
    result = parse_scan(dict)
    return result

if __name__ == "__main__":
    if len(argv) < 2:
        print("Usage: py parse_scan.py <file>; e.g. py scan.py seed/10.1.0.1.json")
        exit(1)
    result = parse_from_JSON(argv[1])
    print(result)
    f = open("parsed/test.json", "w")
    json.dump(result, f , indent=6)
    
