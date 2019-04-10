from mirrulations_core.api_call import add_api_key
from mirrulations_core.api_call_management import api_call_manager
import json
from mirrulations_core.mirrulations_logging import logger
import mirrulations_core.config as config

workfiles = []
version = 'v1.3'

key = config.read_value('key')
client_id = config.read_value('client_id')


def documents_processor(urls, job_id, client_id):
    """
    Call each url in the list, process the results of
    the calls and then form a json file to send back the results
    :param urls: list of urls that have to be called
    :param job_id: the id of the job that is being worked on currently
    :param client_id: id of the client calling this function
    :return result: the json to be returned
            to the server after each call is processed
    """
    global workfiles
    workfiles = []
    for url in urls:
        try:
            result = api_call_manager(add_api_key(url))
            process_results(result)
        except Exception:
            logger.error('Error - URL processing failed')

    result = json.loads(json.dumps({'job_id': job_id,
                                    'type': 'docs',
                                    'data': workfiles,
                                    'client_id': client_id,
                                    'version': version}))
    return result


def process_results(result):
    """
    Loads the json from the results of the api call
    Gets the list of documents from the json
    Creates a new json that contains the documents returned from each api call
    :param result: Result of the api call
    :return: returns True if the processing completed successfully
    """
    docs_json = result.json()
    try:
        doc_list = docs_json['documents']
        work = make_docs(doc_list)
    except TypeError:
        logger.error('Error - cannot process JSON results')

    return True


def make_docs(doc_list):
    """
    Given a list of document jsons that contain the id and the attachment count
    Add the ids to lists that will contain calls that in
    total have no more than 1000 predicted API calls
    :param doc_list: list of document ids and attachment counts as a dictionary
    :return: the global workfiles variable that
             contains all of the work in list
    """
    global workfiles
    size = 0
    work_list = []
    for doc in doc_list:
        doc_id = doc['documentId']
        calls = doc['attachmentCount'] + 1
        if size + calls > 1000:
            workfiles.append(work_list)
            work_list = []
            size = 0
        size += calls
        document = {'id': doc_id, 'count': calls}
        work_list.append(document)
    if size != 0:
        workfiles.append(work_list)
    return workfiles


class BadJsonException(Exception):
    """
    Raised if the json is not correctly formatted or is empty
    """
    pass
