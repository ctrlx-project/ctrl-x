from flask import request
import requests
import pytest
from main import app
from api import api

import os 

"""
@pytest.fixture
def client():
    with api.test_client() as client:
        yield client

class TestIndext:
    def test_index(self, client):
        res = client.get('/')
        assert res.status_code == 200

def test_index():
    app_instance = create_app()
    with app_instance.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200 """

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
