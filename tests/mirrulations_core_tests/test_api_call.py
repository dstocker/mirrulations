import pytest
import requests_mock

from mirrulations_core.api_call import call,\
                                       client_add_api_key,\
                                       server_add_api_key,\
                                       ApiCountZeroException,\
                                       PermanentException,\
                                       TemporaryException

base_url = 'https://api.data.gov:443/regulations/v3/documents.json?'


@pytest.fixture
def mock_req():
    with requests_mock.Mocker() as m:
        yield m


def test_happy_path(mock_req):
    mock_req.get(client_add_api_key(base_url), status_code=200, text='{}')
    assert call(client_add_api_key(base_url)).text == '{}'

    mock_req.get(server_add_api_key(base_url), status_code=200, text='{}')
    assert call(client_add_api_key(base_url)).text == '{}'


def test_exception_thrown(mock_req):
    mock_req.get(client_add_api_key(base_url), status_code=300)
    with pytest.raises(TemporaryException):
        call(client_add_api_key(base_url))

    mock_req.get(server_add_api_key(base_url), status_code=300)
    with pytest.raises(TemporaryException):
        call(server_add_api_key(base_url))


def test_api_count_zero(mock_req):
    mock_req.get(client_add_api_key(base_url), status_code=429)
    with pytest.raises(ApiCountZeroException):
        call(client_add_api_key(base_url))

    mock_req.get(server_add_api_key(base_url), status_code=429)
    with pytest.raises(ApiCountZeroException):
        call(server_add_api_key(base_url))


def test_api_permanent_exception(mock_req):
    mock_req.get(client_add_api_key(base_url), status_code=404)
    with pytest.raises(PermanentException):
        call(client_add_api_key(base_url))

    mock_req.get(server_add_api_key(base_url), status_code=404)
    with pytest.raises(PermanentException):
        call(server_add_api_key(base_url))


def test_invalid_key_gives_permanent_exception(mock_req):
    mock_req.get(client_add_api_key(base_url), status_code=403)
    with pytest.raises(PermanentException):
        call(client_add_api_key(base_url))

    mock_req.get(server_add_api_key(base_url), status_code=403)
    with pytest.raises(PermanentException):
        call(server_add_api_key(base_url))


def test_generic_500_failure(mock_req):
    mock_req.get(client_add_api_key(base_url), status_code=500)
    with pytest.raises(PermanentException):
        call(client_add_api_key(base_url))

    mock_req.get(server_add_api_key(base_url), status_code=500)
    with pytest.raises(PermanentException):
        call(server_add_api_key(base_url))
