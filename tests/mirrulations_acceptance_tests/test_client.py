from flask import Flask, request
import random
import string
import json
import time
from multiprocessing import Process
from mirrulations_core.mirrulations_logging import logger
from mirrulations_client.client_runner import do_work

app = Flask(__name__)
version = 'v1.3'

data_queue = ["https://api.data.gov/regulations/v3/documents.json?rpp=5&po=0"]


@app.route('/')
def default():
    return None


@app.route('/get_work')
def get_work():
    logger.warning('Successful API Call: %s', 'get_work: get_work')
    if len(request.args) != 1:
        logger.error('Incorrect number of parameters')
        return 'Parameter Missing', 400
    client_id = request.args.get('client_id')
    if client_id is None:
        logger.warning('Exception: %s',
                       'get_work: BadParameterException, '
                       'client id was none')
        logger.error('Error - no client ID')
        return 'Bad Parameter', 400

    job_id = ''.join(random.choice(string.ascii_uppercase + string.digits)
                     for _ in range(16))
    type = "docs"
    data = data_queue.pop()
    converted_json = {
        'job_id': job_id,
        'type': type,
        'data': data,
        'version': version
    }
    json_info = json.dumps(converted_json)
    return json_info


@app.route('/return_docs', methods=['POST'])
def return_docs():
    try:
        json_info = request.form['json']
        files = request.files['file'].read()
    except Exception:
        logger.error('Error - bad parameter')
        return 'Bad Parameter', 400
    if json_info is None:
        logger.error('Error - Could not post docs')
        return 'Bad Parameter', 400
    # files = io.BytesIO(files)
    # process_docs(redis_server(), json.loads(json_info), files)
    return 'Successful!'


@app.route('/return_doc', methods=['POST'])
def return_doc():
    return None


def test_client():

    p = Process(target=app.run, args=('0.0.0.0', '8080'))
    p.start()
    time.sleep(1)  # delay to allow server to start

    for _ in range(len(data_queue)):
        do_work()

    p.terminate()

    assert True
