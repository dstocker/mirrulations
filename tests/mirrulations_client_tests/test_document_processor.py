from mirrulations_core.api_call_management import api_call_manager
from mirrulations_client.document_processor import make_doc_url,\
                                                   get_extra_documents,\
                                                   save_document,\
                                                   download_document
import pytest
import requests_mock
import os
import tempfile

from mirrulations_core.api_call import client_add_api_key

import mirrulations_core.config as config

key = config.client_read_value('key')

base_url = 'https://api.data.gov/regulations/v3/document?documentId='


@pytest.fixture
def mock_req():
    with requests_mock.Mocker() as m:
        yield m


@pytest.fixture()
def workfile_tempdir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname


def test_make_doc_url():
    assert base_url + 'DOCUMENTID' == make_doc_url('DOCUMENTID')


def test_collect_extra_documents(mock_req, workfile_tempdir):
    mock_req.get(client_add_api_key(
        make_doc_url("DOCUMENT")),
        status_code=200, text='{ "fileFormats": '
                              '["https://api.data.gov/regulations/v3/download?'
                              'documentId=OSHA-H117-2006-0947-0647&'
                              'attachmentNumber=1&contentType=pdf"] }')
    mock_req.get(client_add_api_key(
        "https://api.data.gov/regulations/v3/download?documentId="
        "OSHA-H117-2006-0947-0647&attachmentNumber=1&contentType=pdf"),
                 status_code=200, text='Document!')
    result = get_extra_documents(api_call_manager(
        client_add_api_key(make_doc_url("DOCUMENT"))),
        workfile_tempdir, "OSHA-H117-2006-0947-0647")

    assert result == 1


def test_collect_attachments(mock_req, workfile_tempdir):
    mock_req.get(client_add_api_key(
        make_doc_url("DOCUMENT")),
        status_code=200, text='{ "attachments": [ '
                              '{ "fileFormats": [ '
                              '"https://api.data.gov/regulations/v3/'
                              'download?documentId='
                              'FDA-2015-N-0540-0004&attachmentNumber=1'
                              '&contentType=msw12", '
                              '"https://api.data.gov/regulations/v3/'
                              'download?documentId='
                              'FDA-2015-N-0540-0004&attachmentNumber=1&'
                              'contentType=pdf" '
                              '] } ] }')
    mock_req.get(client_add_api_key(
        "https://api.data.gov/regulations/v3/download?documentId"
        "=FDA-2015-N-0540-0004&attachmentNumber=1&contentType=msw12"),
                 status_code=200, text='Document!')
    mock_req.get(client_add_api_key(
        "https://api.data.gov/regulations/v3/download?documentId="
        "FDA-2015-N-0540-0004&attachmentNumber=1&contentType=pdf"),
                 status_code=200, text='Document!')

    result = get_extra_documents(api_call_manager(client_add_api_key(
        make_doc_url("DOCUMENT"))), workfile_tempdir, "FDA-2015-N-0540-0004")

    assert result == 1


def test_save_document(workfile_tempdir):
    result = "This is another test"
    documentId = "0000-0000-0067"
    save_document(workfile_tempdir, result, documentId)
    with open(workfile_tempdir + "/doc." +
              documentId + ".json", 'r') as f:
        assert f.readline().strip() == '"This is another test"'


def test_download_document(workfile_tempdir, mock_req):
    url = "https://api.data.gov/regulations/v3/download?documentId=" \
          "FDA-2015-N-0540-0004&attachmentNumber=1&contentType=msw12"
    mock_req.get(client_add_api_key(url), status_code=200, reason="")
    result = api_call_manager(client_add_api_key(url))
    type = "msw12"
    download_document(workfile_tempdir, "FDA-2015-N-0540-0004", result, type)
    assert os.path.exists(workfile_tempdir + "/doc.FDA-2015-N-0540-0004.doc")
