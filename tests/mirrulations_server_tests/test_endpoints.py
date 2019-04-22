import pytest
import requests_mock
import fakeredis
import mirrulations_server.endpoints as endpoints
import json
import os
from ast import literal_eval

PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                    "../test_files/mirrulations_files/filename.txt")

version = 'v1.3'


@pytest.fixture
def mock_req():
    with requests_mock.Mocker() as m:
        yield m


@pytest.fixture
def client():
    endpoints.app.config['TESTING'] = True
    client = endpoints.app.test_client()
    yield client


def make_json():
    return {
        "job_id": 1,
        "client_id": 2,
        "data": [
            [
                {
                    "id": 1, "attachment_count": 1
                 }
            ],
            [
                {
                    "id": 2, "attachment_count": 2
                 }
            ]
        ],
        "version": version
    }


def make_database():
    r = fakeredis.FakeRedis()
    r.flushall()
    test_list = json.dumps(["a", ["b", "c"]])
    r.lpush("queue", test_list)
    return r


def test_default_path(client):
    result = client.get('/')
    assert result.status_code == 200


def test_non_existent_endpoint(client):
    result = client.get('/not_existent')
    assert result.status_code == 404


def test_get_work_success(client):
    result = client.get('/get_work', query_string={'client_id': '1'})
    assert result.status_code == 200


def test_get_work_throws_exception_if_no_client_id(client):
    result = client.get('/get_work')
    assert result.status_code == 400


def test_get_work_wrong_parameter(client):
    result = client.get('/get_work', query_string={'clientid': '1'})
    assert result.status_code == 400


def test_get_queue_item(client):
    r = make_database()
    list = literal_eval(r.lpop("queue").decode("utf-8"))
    assert list == ['a', ['b', 'c']]


def test_generate_json():
    list = ["a", "b", ["a", "b"]]
    json1 = endpoints.generate_json(list)
    assert json1 == json.dumps({"job_id": "a", "type": "b", "data": [
        "a", "b"], "version": version})


def test_return_docs_call_success(client):
    result = client.post("/return_docs", data={'file': open(
        PATH, 'rb'), 'json': json.dumps(make_json())})
    assert result.status_code == 200


def test_return_docs_no_parameter(client):
    result = client.post('/return_docs')
    assert result.status_code == 400


def test_return_doc_call_success(client):
    result = client.post('/return_doc', data={'file': open(
        PATH, 'rb'), 'json': json.dumps(make_json())})
    assert result.status_code == 200


def test_return_doc_no_file_parameter(client):
    result = client.post('/return_doc', data=dict(
        json_info=json.dumps(make_json())))
    assert result.status_code == 400


def test_return_doc_no_json_parameter(client):
    result = client.post('/return_doc', data=dict(file=open(PATH, 'rb')))
    assert result.status_code == 400
