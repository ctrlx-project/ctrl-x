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


def parse_scan(dict):
    scan = dict.get("scan")
    if not scan:
        print("Invalid file")
        return False
    for network in scan.keys():
        print(network)
    return True

if __name__ == "__main__":
    if len(argv) < 2:
        print("Usage: py parse_scan.py <file>; e.g. py scan.py seed/10.1.0.1.json")
        exit(1)
    dict = loadJSON(argv[1])
    result = parse_scan(dict)
    if not result:
        exit(1)
