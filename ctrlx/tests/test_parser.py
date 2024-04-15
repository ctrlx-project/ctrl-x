import json
import pprint
import pytest

import sys
sys.path.append('../') 

import parse_scan

SCAN_PATH = "../seed/nmap/10.10.0.14.json"
PARSED_SCAN = "../seed/scan_parser/10.10.0.14.json"

with open(SCAN_PATH, encoding="UTF-8") as json_scan:
    SCAN = json.load(json_scan)
with open(SCAN_PATH, encoding="UTF-8") as json_parsed:
    PARSED_SCAN = json.load(json_parsed)

def test_load_json():
    """Tests load_json function."""
    loaded_json = parse_scan.loadJSON(SCAN_PATH)
    assert loaded_json == SCAN

def test_get_cve():
    """Tests get_cve function."""
    expected_cves = PARSED_SCAN["10.10.0.14"]["ports"]["80"]["script"]["vulner"]
    cves = parse_scan.get_CVE(SCAN["scan"]["10.10.0.14"]["tcp"]["80"]["script"]["vulners"])
    assert cves == expected_cves

def test_parse_scan():
    """Tests parse_scan function."""
    result = parse_scan.parse_scan(SCAN)
    assert PARSED_SCAN == result

pprint.pprint(parse_scan.parse_scan(SCAN))
test_load_json()
test_get_cve()
test_parse_scan()
