from io import BytesIO
import json
import os
import random
from mock import patch
from requests_mock import mock as req_mock
import string
import tempfile
import zipfile
from mirrulations_core.api_call import client_add_api_key
import mirrulations_core.config as config
from mirrulations_client.client_runner import do_work

version = 'v1.3'


def test_docs_client():

    job_id = ''.join(random.choice(string.ascii_uppercase + string.digits)
                     for _ in range(16))

    server_url = 'http://'\
                 + config.client_read_value('ip')\
                 + ':'\
                 + config.client_read_value('port')\
                 + '/get_work?client_id='\
                 + config.client_read_value('client id')
    docs_url = 'https://api.data.gov/regulations/v3/documents.json?rpp=5&po=0'
    client_health_url = 'https://hc-ping.com/457a1034-83d4-4a62-8b69-c71060db3a08'

    server_dict = {'job_id': job_id,
                   'type': 'docs',
                   'data': [docs_url],
                   'version': version}
    docs_dict = {'documents': [{'attachmentCount': 0,
                                'documentId': 'TEST-0-0'},
                               {'attachmentCount': 1,
                                'documentId': 'TEST-0-1'},
                               {'attachmentCount': 2,
                                'documentId': 'TEST-0-2'},
                               {'attachmentCount': 3,
                                'documentId': 'TEST-0-3'},
                               {'attachmentCount': 4,
                                'documentId': 'TEST-0-4'}]}
    result_dict = [[{'id': 'TEST-0-0',
                     'count': 1},
                    {'id': 'TEST-0-1',
                     'count': 2},
                    {'id': 'TEST-0-2',
                     'count': 3},
                    {'id': 'TEST-0-3',
                     'count': 4},
                    {'id': 'TEST-0-4',
                     'count': 5}]]

    with req_mock() as m,\
            patch('requests.post') as p:

        m.get(server_url,
              status_code=200,
              text=json.dumps(server_dict))
        m.get(client_add_api_key(docs_url),
              status_code=200,
              text=json.dumps(docs_dict))
        m.get(client_health_url,
              status_code=200)

        do_work()
        assert json.loads(p.call_args[1]['data']['json'])['data'] == result_dict


def test_doc_client():
    job_id = ''.join(random.choice(string.ascii_uppercase + string.digits)
                     for _ in range(16))

    server_url = 'http://' \
                 + config.client_read_value('ip') \
                 + ':' \
                 + config.client_read_value('port') \
                 + '/get_work?client_id=' \
                 + config.client_read_value('client id')
    doc_url = 'https://api.data.gov/regulations/v3/document?documentId=TEST-1-0'
    doc_url_with_download = doc_url + '&attachmentNumber=0&contentType=pdf'
    client_health_url = 'https://hc-ping.com/457a1034-83d4-4a62-8b69-c71060db3a08'

    server_dict = {'job_id': job_id,
                   'type': 'doc',
                   'data': [{'id': 'TEST-1-0', 'count': 1}],
                   'version': version}
    doc_text = json.dumps({'fileFormats': [doc_url_with_download]})

    with req_mock() as m, \
            patch('requests.post') as p:

        m.get(server_url,
              status_code=200,
              text=json.dumps(server_dict))
        m.get(client_add_api_key(doc_url),
              status_code=200,
              text=doc_text)
        m.get(client_add_api_key(doc_url_with_download),
              status_code=200,
              body=open(config.server_read_value('regulations path')
                        + 'TEST-1-0.pdf'))
        m.get(client_health_url,
              status_code=200)

        do_work()

        temp_directory = tempfile.mkdtemp()
        temp_directory_path = str(temp_directory) + '/'

        files = zipfile.ZipFile(BytesIO(p.call_args[1]['files']['file'][1].read()), 'r')
        files.extractall(temp_directory_path)
        file_list = os.listdir(temp_directory_path)

        assert 'mirrulations.log' in file_list
        assert 'doc.TEST-1-0.json' in file_list
        assert 'doc.TEST-1-0.pdf' in file_list
