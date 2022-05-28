import os
import requests
from openapi_spec_validator import validate_spec_url

def test_history(api_v1_host):
    endpoint = os.path.join(api_v1_host, 'history', 'test')
    response = requests.get(endpoint)
    assert response.status_code == 200
    json = response.json()
    assert 'msg' in json
    assert json['msg'] == "I'm the test endpoint from history."

def test_graph(api_v1_host):
    endpoint = os.path.join(api_v1_host, 'graph', 'test')
    response = requests.get(endpoint)
    assert response.status_code == 200
    json = response.json()
    assert 'msg' in json
    assert json['msg'] == "I'm the test endpoint from graph."

def test_history_get(api_v1_host):
    endpoint = os.path.join(api_v1_host, 'history', 'get')
    payload = {'number': 5}
    response = requests.post(endpoint, json=payload)
    assert response.status_code == 200
    json = response.json()
    assert 'msg' in json
    assert json['msg'] == "Your result is: '10'"

def test_history_manage(api_v1_host):
    endpoint = os.path.join(api_v1_host, 'history', 'manage')
    payload = {'number': 5}
    response = requests.post(endpoint, json=payload)
    assert response.status_code == 200
    json = response.json()
    assert 'msg' in json
    assert json['msg'] == "Your result is: '10'"

def test_swagger_specification(host):
    endpoint = os.path.join(host, 'api', 'swagger.json')
    validate_spec_url(endpoint)
    # use https://editor.swagger.io/ to fix issues
