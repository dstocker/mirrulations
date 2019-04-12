import mirrulations_client.document_processor as doc
import mirrulations_client.documents_processor as docs
import mirrulations_core.api_call_management as man
import requests
import json
import time
import shutil
import tempfile
from pathlib import Path
import mirrulations_core.config as config
from mirrulations_core.mirrulations_logging import logger

# These variables are specific to the current implementation
version = 'v1.3'

client_health_url = 'https://hc-ping.com/457a1034-83d4-4a62-8b69-c71060db3a08'


def get_work(server_url, client_id):
    """
    Calls the /get_work endpoint of the server to fetch work to process
    :param client_id: the id of the client calling /get_work
    :return: the result of making a call to get work
    """
    url = server_url + '/get_work?client_id=' + client_id
    result = man.api_call_manager(url)
    logger.warning('Obtained work from server.')
    return result


def get_json_info(json_result):
    """
    Return job information from server json
    :param json_result: the json returned from
    :return:
    """

    job_id = json_result['job_id']
    urls = json_result['data']
    return job_id, urls


def return_docs(json_result, server_url, client_id):
    """
    Handles the documents processing necessary for a job
    Calls the /return_docs endpoint of the
    server to return data for the job it completed
    :param json_result: the json received from the /get_work endpoint
    :param client_id: the id of the client that is processing the documents job
    :return: result from calling /return_docs
    """

    job_id, urls = get_json_info(json_result)
    json_info = docs.documents_processor(urls, job_id, client_id)
    path = tempfile.TemporaryDirectory()
    add_client_log(path.name)
    shutil.make_archive('result', 'zip', path.name)
    fileobj = open('result.zip', 'rb')
    r = requests.post(server_url + '/return_docs',
                      files={'file': fileobj},
                      data={'json': json.dumps(json_info)})
    r.raise_for_status()
    logger.warning('Client returned docs')
    logger.handlers[0].doRollover()
    return r


def return_doc(json_result, server_url, client_id):
    """
    Handles the document processing necessary for a job
    Calls the /return_doc endpoint of the server
    to return data for the job it completed
    :param json_result: the json received from the /get_work endpoint
    :param client_id: the id of the client that is processing the documents job
    :return: result from calling /return_doc
    """

    job_id, doc_dicts = get_json_info(json_result)
    doc_ids = []
    for dic in doc_dicts:
        doc_ids.append(dic['id'])
    path = doc.document_processor(doc_ids)
    add_client_log(path.name)
    shutil.make_archive('result', 'zip', path.name)
    fileobj = open('result.zip', 'rb')
    r = requests.post(server_url+'/return_doc',
                      files={'file': ('result.zip', fileobj)},
                      data={'json': json.dumps({'job_id': job_id,
                                                'type': 'doc',
                                                'user': client_id,
                                                'version': version})})
    r.raise_for_status()
    logger.warning('Client returned doc')
    logger.handlers[0].doRollover()
    return r


def add_client_log(directory_to_send_to, filepath='./mirrulations.log'):
    """
    Safely copies a file to a directory;
    if the file isn't there to be copied, it won't be copied.
    :param directory_to_send_to: Directory to copy to
    :param filepath: File to copy
    """

    if Path(filepath).exists():
        if Path(directory_to_send_to).exists():
            shutil.copy(filepath, directory_to_send_to)
            logger.warning('mcl/client/add_client_log: '
                           'mirrulations.log successfully copied')
        else:
            logger.warning('File not copied, '
                           'directory_to_send_to does not exist')
    else:
        logger.warning('File not copied, file does not exist')


def do_work():
    """
    Working loop
    Get work - Determine type of work - Do work - Return work
    If there is no work in the server, sleep for an hour
    :return:
    """

    ip = config.client_read_value('ip')
    port = config.client_read_value('port')
    client_id = config.client_read_value('client id')

    server_url = 'http://' + ip + ':' + port

    while True:
        try:
            work = get_work(server_url, client_id)
            requests.get(client_health_url)
            work_json = json.loads(work.content.decode('utf-8'))
        except man.CallFailException:
            time.sleep(3600)
            continue
        if work_json['type'] == 'doc':
            r = return_doc(work_json, server_url, client_id)
            requests.get(client_health_url)
        elif work_json['type'] == 'docs':
            r = return_docs(work_json, server_url, client_id)
            requests.get(client_health_url)
        elif work_json['type'] == 'none':
            time.sleep(3600)
            requests.get(client_health_url)
        else:
            logger.error('Error - Job type unexpected')
            requests.get(client_health_url + '/fail')


if __name__ == '__main__':
    do_work()
