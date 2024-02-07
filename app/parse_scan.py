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
    try:
        result = obj.get(field)
        if result is None:
            print("Failed scan")
            # print(field)
    except:
        result = None
    return result


def parse_scan(dict):
    result = {}
    scan = safe_get(dict, "scan")
    if scan is None:
        return None
    if (len(scan.keys())!=1):
        print("Failed scan")
        return None
    for network in scan.keys():
        network_result = safe_get(scan, network)
        state = safe_get(safe_get(network_result, "status"), "state")
        if state is None:
            return None
        result["network"] = {"state", state}
        if (state != "up"):
            return None
        fields = ["tcp", "udp"]
        
    return result



    return True

if __name__ == "__main__":
    if len(argv) < 2:
        print("Usage: py parse_scan.py <file>; e.g. py scan.py seed/10.1.0.1.json")
        exit(1)
    dict = loadJSON(argv[1])
    result = parse_scan(dict)
    print(result)
