from flask import request
from werkzeug.datastructures import Headers
import requests
import pytest
from main import app
from api import api
import json

import os 
os.environ['CONFIG_TYPE'] = 'config.TestingConfig'

def test_home_page():
    with app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200

def test_api_test_mq():
    with app.test_client() as test_client:
        response = test_client.get('api/test-scan')
        res_body = json.loads(response.data.decode('utf-8'))
        assert response.status_code == 200 and res_body["message"] == "Ping"

def test_api_scan():
    with app.test_client() as test_client:
        response = test_client.get('api/scan')
        res_body = json.loads(response.data.decode('utf-8'))
        assert response.status_code == 200 and res_body != {}

def test_api_scan_new():
    with app.test_client() as test_client:
        response = test_client.post('api/scan-new', data = {'ip_block': '0.0.0.0'})
        res_body = json.loads(response.data.decode('utf-8'))
        assert response.status_code == 200 and res_body["status"] != "error"