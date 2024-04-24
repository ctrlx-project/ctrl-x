from flask import request
import requests
import pytest
from main import app
from api import api
import json

import os 

def test_home_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    # Set the Testing configuration prior to creating the Flask application
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    #flask_app.run()

    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200

def test_api_test_mq():
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    with app.test_client() as test_client:
        response = test_client.get('api/test-scan')
        res_body = json.loads(response.data.decode('utf-8'))
        assert res_body["message"] == "Ping"
