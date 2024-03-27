from flask import request
import requests
import pytest
from app import create_app
from api import api

@pytest.fixture
def client():
    with api.test_client() as client:
        yield client

class TestIndext:
    def test_index(self, client):
        res = client.get('/')
        assert res.status_code == 200
"""
def test_index():
    app_instance = create_app()
    with app_instance.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200 """
