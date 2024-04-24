"""Tests the parse_scan module."""

import json
import os
import pytest

import parse_scan

directory = os.path.dirname(__file__)
SCAN_PATH = os.path.join(directory, "seed/nmap/10.10.0.14.json")
PARSED_SCAN_PATH = os.path.join(directory, "seed/scan_parser/10.10.0.14.json")

with open(SCAN_PATH, encoding="UTF-8") as json_scan:
    SCAN = json.load(json_scan)
with open(PARSED_SCAN_PATH, encoding="UTF-8") as json_parsed:
    PARSED_SCAN = json.load(json_parsed)

def test_load_json():
    """Tests load_json function."""
    loaded_json = parse_scan.load_json(SCAN_PATH)
    assert loaded_json == SCAN

def test_get_cve():
    """Tests get_cve function."""
    expected_cves = PARSED_SCAN["10.10.0.14"]["ports"]["80"]["vulner"]
    cves = parse_scan.get_cve(SCAN["scan"]["10.10.0.14"]["tcp"]["80"]["script"]["vulners"])
    assert cves == expected_cves

def test_parse_scan():
    """Tests parse_scan function."""
    result = parse_scan.parse_scan(SCAN)
    assert PARSED_SCAN == result

def test_parse_from_json():
    """Tests parse_from_json function."""
    result = parse_scan.parse_from_json(SCAN_PATH)
    assert PARSED_SCAN == result
