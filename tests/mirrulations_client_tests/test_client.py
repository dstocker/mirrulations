from flask import Flask, request
import json
from multiprocessing import Process
import random
from requests_mock import mock as req_mock
import string
import time
from mirrulations_core.api_call import client_add_api_key
from mirrulations_client.client_runner import do_work

app = Flask(__name__)
version = 'v1.3'

test_queue = [['docs', ['https://api.data.gov/regulations/v3/documents.json?rpp=5&po=0']]]
call_zero = json.dumps({'documents': [{'attachmentCount': 0,
                                            'documentId': 'TEST-0-0'},
                                           {'attachmentCount': 1,
                                            'documentId': 'TEST-0-1'},
                                           {'attachmentCount': 2,
                                            'documentId': 'TEST-0-2'},
                                           {'attachmentCount': 3,
                                            'documentId': 'TEST-0-3'},
                                           {'attachmentCount': 4,
                                            'documentId': 'TEST-0-4'}]})
result_zero = [[{"id": "TEST-0-0", "count": 1},
                     {"id": "TEST-0-1", "count": 2},
                     {"id": "TEST-0-2", "count": 3},
                     {"id": "TEST-0-3", "count": 4},
                     {"id": "TEST-0-4", "count": 5}]]

@app.route('/')
def default():
    return None


@app.route('/get_work')
def get_work():

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

    if json.loads(json_info)['data'] == result_zero:
        return 'Successful!'
    else:
        return 'Failure!', 400


@app.route('/return_doc', methods=['POST'])
def return_doc():
    return None


def test_client():

    p = Process(target=app.run, args=('0.0.0.0', '8080'))
    p.start()
    time.sleep(1)  # delay to allow server to start

    with req_mock(real_http=True) as m:
        m.get(client_add_api_key(test_queue[0][1][0]),
              status_code=200,
              text=call_zero)

        for _ in range(len(test_queue)):
            do_work()

        p.terminate()

    assert True
