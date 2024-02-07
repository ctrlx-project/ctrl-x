import json
from sys import argv


def loadJSON(filepath):
    try:
        f = open(filepath, "r")
    except:
        print("File does not exist")
        exit(1)
    dict = json.load(f)
    return dict


def safe_get(obj, field):
    result = obj.get(field)
    if not result:
        print("Invalid scan result")
        exit(1)
    return result


def parse_scan(dict):
    scan = safe_get(dict, "scan")
    result = {}
    if (len(scan.keys())!=1):
        print("Invalid scan result")
        exit(1)
    for network in scan.keys():
        network_result = safe_get(dict, network)
        state = safe_get(safe_get(network_result, "status"), "state")
        result["network"] = {"state", state}
        if (state != "up"):
            break
        
    return result



    return True

if __name__ == "__main__":
    if len(argv) < 2:
        print("Usage: py parse_scan.py <file>; e.g. py scan.py seed/10.1.0.1.json")
        exit(1)
    dict = loadJSON(argv[1])
    result = parse_scan(dict)
    if not result:
        exit(1)
