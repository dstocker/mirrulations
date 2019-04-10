from mirrulations_client.client import get_work,\
                                       return_doc,\
                                       return_docs,\
                                       add_client_log
import pytest
import requests_mock
import tempfile
from mirrulations_core.api_call import add_api_key
from mirrulations_core.api_call_management import CallFailException
import mirrulations_core.config as config


def get_client_id():
    return config.read_value('client_id')


def get_server_address():
    return "http://" + config.read_value('ip') +\
           ":" + config.read_value('port')


@pytest.fixture
def mock_req():
    with requests_mock.Mocker() as m:
        yield m


def test_get_work(mock_req, caplog):
    url = get_server_address() + "/get_work?client_id=" + get_client_id()
    mock_req.get(url, status_code=200, text='RANDOM')
    result = get_work(get_server_address(), get_client_id())
    assert result.status_code == 200
    assert 'Obtained work from server.' in caplog.text


def test_return_docs(mock_req):
    mock_req.post(get_server_address() + "/return_docs", status_code=200)
    mock_req.get(add_api_key(
        'http://website.com/random'), status_code=200, text='{"documents": \
            [{"documentId": "CMS-2005-0001-0001", "attachmentCount": 4},\
            {"documentId": "CMS-2005-0001-0002", "attachmentCount": 999}]}')
    r = return_docs({'job_id': 'qwerty', 'data':
                    ['http://website.com/random']},
                    get_server_address(), get_client_id())
    assert r.status_code == 200


def ignore_test_return_docs_error(mock_req):
    mock_req.get(add_api_key('http://website.com/random'),
                 status_code=400, text='{"documents": \
            [{"documentId": "CMS-2005-0001-0001", "attachmentCount": 4},\
            {"documentId": "CMS-2005-0001-0002", "attachmentCount": 999}]}')
    with pytest.raises(CallFailException):
        r = return_docs({'job_id': 'qwerty', 'data':
                        ['http://website.com/random']},
                        get_server_address(), get_client_id())


def test_return_doc(mock_req):
    mock_req.post(get_server_address() + "/return_doc", status_code=200)

    mock_req.get(add_api_key(
        'https://api.data.gov/regulations/v3/document?documentId=website-com'),
        status_code=200, text='{ "something": '
                              '["https://api.data.gov/regulations/v3/download?'
                              'documentId=OSHA-H117-2006-0947-0647&'
                              'attachmentNumber=1&contentType=pdf"] }')
    r = return_doc({'job_id':
                    'qwerty', 'data': [{'id': 'website-com',
                                        'count': 4}]}, get_server_address(),
                   get_client_id())

    assert r.status_code == 200


def test_add_logs():
    path = tempfile.TemporaryDirectory()
    zip_path = tempfile.TemporaryDirectory()

    open(path.name + "/mirrulations.log", "w").write("test")

    add_client_log(zip_path.name, path.name + '/mirrulations.log')

    assert open(zip_path.name + "/mirrulations.log", "r").read() == "test"

    path.cleanup()
    zip_path.cleanup()
