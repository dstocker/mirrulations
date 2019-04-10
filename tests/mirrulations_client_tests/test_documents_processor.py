from mirrulations_client.documents_processor import documents_processor,\
                                                    make_docs,\
                                                    process_results
import json
import pytest
import requests_mock

from mirrulations_core.api_call import add_api_key
from mirrulations_core.api_call_management import api_call_manager,\
                                                  CallFailException
import mirrulations_core.config as config

key = config.read_value('key')
client_id = config.read_value('client_id')

base_url = 'https://api.data.gov:443/regulations/v3/documents.json?'
base_url2 = 'https://www.website.com/regulations/v3/documents.json?'

version = 'v1.3'


@pytest.fixture
def mock_req():
    with requests_mock.Mocker() as m:
        yield m


def test_documents_processor_basic():
    urls = []
    docs = documents_processor(urls, 'JobID', client_id)
    assert docs == {'client_id': client_id, "type": "docs",
                    'data': [],
                    'job_id': 'JobID',
                    'version': version}


def test_make_docs_complex():
    test = make_docs([{"documentId": "QWERTYUIOP0", "attachmentCount": 998},
                      {"documentId": "QWERTYUIOP1", "attachmentCount": 9},
                      {"documentId": "QWERTYUIOP2", "attachmentCount": 8},
                      {"documentId": "QWERTYUIOP3", "attachmentCount": 7},
                      {"documentId": "QWERTYUIOP4", "attachmentCount": 6},
                      {"documentId": "QWERTYUIOP5", "attachmentCount": 5},
                      {"documentId": "QWERTYUIOP6", "attachmentCount": 4}])
    assert test == [[{"id": "QWERTYUIOP0", "count": 999}],
                    [{"id": "QWERTYUIOP1", "count": 10},
                     {"id": "QWERTYUIOP2", "count": 9},
                     {"id": "QWERTYUIOP3", "count": 8},
                     {"id": "QWERTYUIOP4", "count": 7},
                     {"id": "QWERTYUIOP5", "count": 6},
                     {"id": "QWERTYUIOP6", "count": 5}]]


def test_documents_processor_empty():
    urls = []
    docs = documents_processor(urls, 'JobID', client_id)
    assert docs == {'client_id': client_id,
                    'type': 'docs',
                    'data': [],
                    'job_id': 'JobID',
                    'version': version}


def test_make_docs():

    test = make_docs([{"documentId": "QWERTYUIOP1", "attachmentCount": 9},
                      {"documentId": "QWERTYUIOP2", "attachmentCount": 8},
                      {"documentId": "QWERTYUIOP3", "attachmentCount": 7},
                      {"documentId": "QWERTYUIOP4", "attachmentCount": 6},
                      {"documentId": "QWERTYUIOP5", "attachmentCount": 5},
                      {"documentId": "QWERTYUIOP6", "attachmentCount": 4}])
    assert test == [[{"id": "QWERTYUIOP1", "count": 10},
                     {"id": "QWERTYUIOP2", "count": 9},
                     {"id": "QWERTYUIOP3", "count": 8},
                     {"id": "QWERTYUIOP4", "count": 7},
                     {"id": "QWERTYUIOP5", "count": 6},
                     {"id": "QWERTYUIOP6", "count": 5}]]


def test_documents_processor(mock_req):
    urls = [base_url, base_url2]
    mock_req.get(add_api_key(base_url),
                 status_code=200, text='{"documents": '
                                       '[{"documentId": '
                                       '"CMS-2005-0001-0001",'
                                       ' "attachmentCount": 4},\
                                       {"documentId": '
                                       '"CMS-2005-0001-0002",'
                                       ' "attachmentCount": 999}]}')
    mock_req.get(add_api_key(base_url2),
                 status_code=200, text='{"documents": '
                                       '[{"documentId": '
                                       '"CMS-2005-0001-0003", '
                                       '"attachmentCount": 88},\
                                         {"documentId": '
                                       '"CMS-2005-0001-0004", '
                                       '"attachmentCount": 666}]}')
    docs = documents_processor(urls, 'Job ID', client_id)
    assert docs == ({'job_id': 'Job ID', 'type': 'docs', 'data': [[{
        'id': 'CMS-2005-0001-0001', 'count': 5}],
                                                  [{'id': 'CMS-2005-0001-0002',
                                                    'count': 1000}],
                                                  [{'id': 'CMS-2005-0001-0003',
                                                    'count': 89},
                                                   {'id': 'CMS-2005-0001-0004',
                                                    'count': 667}]
                                                  ],
                                                    'version': version,
                                                    'client_id': client_id})


def test_valid_results(mock_req):
    urls = [base_url]
    mock_req.get(add_api_key(base_url),
                 status_code=200, text='{"documents": '
                                       '[{"documentId": '
                                       '"CMS-2005-0001-0001", '
                                       '"attachmentCount": 4},\
                                         {"documentId": '
                                       '"CMS-2005-0001-0002", '
                                       '"attachmentCount": 999}]}')
    result = process_results(api_call_manager(add_api_key(base_url)))
    assert result


def test_successful_call(mock_req):
    mock_req.get(base_url, status_code=200, text='{}')
    assert api_call_manager(base_url).text == '{}'


def test_call_fail_raises_exception(mock_req):
    mock_req.get(base_url, status_code=407, text='{}')
    with pytest.raises(CallFailException):
        api_call_manager(base_url)


def test_empty_json(mock_req):
    mock_req.get(base_url, status_code=200, text='')
    with pytest.raises(json.JSONDecodeError):
        process_results(api_call_manager(base_url))


def test_bad_json_format(mock_req):
    mock_req.get(base_url, status_code=200, text='{information: [{},{}]}')
    with pytest.raises(json.JSONDecodeError):
        process_results(api_call_manager(base_url))
