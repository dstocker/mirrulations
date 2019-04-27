from flask import Flask, request
from io import BytesIO
import json
from multiprocessing import Process
import os
import random
from requests_mock import mock as req_mock
import string
import tempfile
import time
import zipfile
from mirrulations_core.api_call import client_add_api_key
import mirrulations_core.config as config
from mirrulations_client.client_runner import do_work

app = Flask(__name__)
version = 'v1.3'

docs_url = 'https://api.data.gov/regulations/v3/documents.json?rpp=5&po=0'
docs_test = ['docs', [docs_url]]
docs_text = json.dumps({'documents': [{'attachmentCount': 0,
                                       'documentId': 'TEST-0-0'},
                                      {'attachmentCount': 1,
                                       'documentId': 'TEST-0-1'},
                                      {'attachmentCount': 2,
                                       'documentId': 'TEST-0-2'},
                                      {'attachmentCount': 3,
                                       'documentId': 'TEST-0-3'},
                                      {'attachmentCount': 4,
                                       'documentId': 'TEST-0-4'}]})
docs_result = [[{'id': 'TEST-0-0', 'count': 1},
                {'id': 'TEST-0-1', 'count': 2},
                {'id': 'TEST-0-2', 'count': 3},
                {'id': 'TEST-0-3', 'count': 4},
                {'id': 'TEST-0-4', 'count': 5}]]

doc_url = 'https://api.data.gov/regulations/v3/document?documentId=TEST-1-0'
doc_url_with_download = doc_url + '&attachmentNumber=0&contentType=pdf'
doc_text = json.dumps({'fileFormats': [doc_url_with_download]})
doc_test = ['doc', [{'id': 'TEST-1-0', 'count': 1}]]
doc_result = []

test_queue = [docs_test, doc_test]


@app.route('/')
def default():
    return None


@app.route('/get_work')
def get_work():
    global test_queue

    if len(request.args) != 1:
        return 'Parameter Missing', 400

    client_id = request.args.get('client_id')
    if client_id is None:
        return 'Bad Parameter', 400

    work = test_queue.pop()
    return json.dumps({
        'job_id': ''.join(random.choice(string.ascii_uppercase + string.digits)
                          for _ in range(16)),
        'type': work[0],
        'data': work[1],
        'version': version
    })


@app.route('/return_docs', methods=['POST'])
def return_docs():
    try:
        json_info = request.form['json']
    except Exception:
        return 'Bad Parameter', 400

    if json.loads(json_info)['data'] == docs_result:
        return 'Successful!'
    else:
        return 'Failure!', 400


@app.route('/return_doc', methods=['POST'])
def return_doc():
    try:
        files_in = BytesIO(request.files['file'].read())
    except Exception:
        return 'Bad Parameter', 400

    temp_directory = tempfile.mkdtemp()
    temp_directory_path = str(temp_directory) + '/'

    files = zipfile.ZipFile(files_in, 'r')
    files.extractall(temp_directory_path)
    file_list = os.listdir(temp_directory_path)

    if file_list == ['doc.TEST-1-0.json', 'doc.TEST-1-0.pdf', 'mirrulations.log']:
        return 'Successful'
    else:
        return 'Failure', 400


def test_client():
    global test_queue

    p = Process(target=app.run, args=('0.0.0.0', '8080'))
    p.start()
    time.sleep(1)  # delay to allow server to start

    with req_mock(real_http=True) as m:
        m.get(client_add_api_key(docs_url),
              status_code=200,
              text=docs_text)
        m.get(client_add_api_key(doc_url),
              status_code=200,
              text=doc_text)
        m.get(client_add_api_key(doc_url_with_download),
              status_code=200,
              body=open(config.server_read_value('regulations path')
                        + 'TEST-1-0.pdf'))

        for _ in range(len(test_queue)):
            do_work()

    p.terminate()

    assert True
