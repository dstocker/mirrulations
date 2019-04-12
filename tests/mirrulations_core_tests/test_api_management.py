import pytest
import requests_mock
from mock import Mock, patch
from mirrulations_core.api_call import client_add_api_key,\
                                       server_add_api_key
from mirrulations_core.api_call_management import api_call_manager,\
                                                  CallFailException

base_url = 'https://api.data.gov:443/regulations/v3/documents.json?'


@pytest.fixture
def mock_req():
    with requests_mock.Mocker() as m:
        yield m


def set_time():
    mock_time = Mock()
    mock_time.return_value = None
    return mock_time


def test_success(mock_req):
    mock_req.get(client_add_api_key(base_url), status_code=200, text='{}')
    assert api_call_manager(client_add_api_key(base_url)).text == '{}'

    mock_req.get(server_add_api_key(base_url), status_code=200, text='{}')
    assert api_call_manager(server_add_api_key(base_url)).text == '{}'


@patch('time.sleep', set_time())
def test_retry_calls_failure(mock_req):
    mock_req.get(client_add_api_key(base_url), status_code=304)
    with pytest.raises(CallFailException):
        api_call_manager(client_add_api_key(base_url))

    mock_req.get(server_add_api_key(base_url), status_code=304)
    with pytest.raises(CallFailException):
        api_call_manager(server_add_api_key(base_url))


def test_callfailexception(mock_req):
    mock_req.get(client_add_api_key(base_url), status_code=403)
    with pytest.raises(CallFailException):
        api_call_manager(client_add_api_key(base_url))

    mock_req.get(server_add_api_key(base_url), status_code=403)
    with pytest.raises(CallFailException):
        api_call_manager(server_add_api_key(base_url))


@patch('time.sleep', set_time())
def test_user_out_of_api_calls_sleeps(mock_req):
    mock_req.register_uri('GET', client_add_api_key(base_url), [{
        'text': 'resp1', 'status_code': 429}, {
        'text': '{}', 'status_code': 200}])
    assert api_call_manager(client_add_api_key(base_url)).text == '{}'

    mock_req.register_uri('GET', server_add_api_key(base_url), [{
        'text': 'resp1', 'status_code': 429}, {
        'text': '{}', 'status_code': 200}])
    assert api_call_manager(server_add_api_key(base_url)).text == '{}'
