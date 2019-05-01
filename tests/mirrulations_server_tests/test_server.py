import json
import os
import pytest
from mirrulations_server.endpoints import app
from mirrulations_server.redis_manager import RedisManager
import shutil
import mirrulations_core.config as config

import mock

PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                    '../test_files/mirrulations_files/')
doc_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                    '../test_files/acceptance/')
def get_count_of_doc():
    count = 0
    for name in os.listdir(config.server_read_value('regulations path') + 'regulations-data/'):
        for org in os.listdir(config.server_read_value('regulations path') + 'regulations-data/'+ name):
            for id in os.listdir(config.server_read_value('regulations path') + 'regulations-data/'+ name + '/' + org):
                for num in os.listdir(config.server_read_value('regulations path') + 'regulations-data/'+ name + '/' + org + '/' + id):
                    if os.path.isfile(config.server_read_value('regulations path') + 'regulations-data/' + name + '/' + org + '/' + id + '/' + num):
                        count += 1
    return count

@pytest.fixture
def client():
    app.config['TESTING'] = True
    yield app.test_client()


def return_data_ids(number_ids):
    return_data_string = '['
    for i in range(0, number_ids):
        return_data_string += '[{"id": "AHRQ_FRDOC_0001-0037", "count": ' + str(number_ids) + '}],'
    return_data_string = return_data_string[:-1]
    return_data_string += ']'
    return return_data_string


def test_root_gives_empty_json(client):
    result = client.get('/')
    assert {} == json.loads(result.data)


def test_when_one_job_in_db_then_job_returned_by_get_work(client):
    rm = RedisManager()
    rm.add_to_queue(json.dumps({'job_id': '1234', 'type': 'docs', 'data': ['Url1'], 'version': '0.5'}))

    result = client.get('/get_work?client_id=asdf')

    assert {'job_id': '1234', 'type': 'docs', 'data': ['Url1'], 'version': '0.5'} == json.loads(result.data)
    assert rm.does_job_exist_in_progress('1234')


def test_when_two_jobs_in_db_returned_by_get_work(client):
    rm = RedisManager()
    rm.add_to_queue(json.dumps({'job_id': '1234', 'type': 'docs', 'data': ['Url1'], 'version': '0.5'}))
    rm.add_to_queue(json.dumps({'job_id': '3456', 'type': 'docs', 'data': ['Url2'], 'version': '0.5'}))

    result = client.get('/get_work?client_id=asdf')
    result_two = client.get('/get_work?client_id=asdf')

    assert {'job_id': '1234', 'type': 'docs', 'data': ['Url1'], 'version': '0.5'} == json.loads(result.data)
    assert {'job_id': '3456', 'type': 'docs', 'data': ['Url2'], 'version': '0.5'} == json.loads(result_two.data)
    assert rm.does_job_exist_in_progress('1234')
    assert rm.does_job_exist_in_progress('3456')


def test_when_two_jobs_in_db_return_one_by_get_work(client):
    rm = RedisManager()
    rm.add_to_queue(json.dumps({'job_id': '1234', 'type': 'docs', 'data': ['Url1'], 'version': '0.5'}))
    rm.add_to_queue(json.dumps({'job_id': '3456', 'type': 'docs', 'data': ['Url2'], 'version': '0.5'}))

    result = client.get('/get_work?client_id=asdf')

    assert {'job_id': '1234', 'type': 'docs', 'data': ['Url1'], 'version': '0.5'} == json.loads(result.data)
    assert rm.does_job_exist_in_progress('1234')
    assert rm.does_job_exist_in_queue('3456')
    assert rm.does_job_exist_in_progress('3456') is False


def test_docs_job_in_db_return_doc_place_in_db_queue(client):
    rm = RedisManager()
    rm.add_to_queue(json.dumps({'data': ['Url1'], 'version': 'v0.5', 'type': 'docs', 'job_id': '1234'}))

    result = client.get('/get_work?client_id=asdf')

    assert {'data': ['Url1'], 'version': 'v0.5', 'type': 'docs', 'job_id': '1234'} == json.loads(result.data)
    assert rm.does_job_exist_in_progress('1234') is True

    client.post('/return_docs',
                data={'file': open(PATH + 'Archive.zip', 'rb'),
                      'json': json.dumps({'job_id': '1234',
                                          'type': 'docs',
                                          'data': [[{'id': 'AHRQ_FRDOC_0001-0037', 'count': 1}]],
                                          'client_id': 'abcd',
                                          'version': '0.5'})})
    assert len(rm.get_all_items_in_queue()) == 1
    assert rm.does_job_exist_in_progress('1234') is False


def test_docs_job_return_multiple_doc_place_in_db_queue(client):
    rm = RedisManager()

    rm.add_to_queue(json.dumps({'data': ['Url1'], 'version': 'v0.5', 'type': 'docs', 'job_id': '1234'}))
    result = client.get('/get_work?client_id=asdf')

    assert {'data': ['Url1'], 'version': 'v0.5', 'type': 'docs', 'job_id': '1234'} == json.loads(result.data)
    assert rm.does_job_exist_in_progress('1234') is True

    client.post('/return_docs',
                data={'file': open(PATH + 'Archive.zip', 'rb'),
                      'json': json.dumps({'job_id': '1234', 'type': 'docs',
                                          'data': [[{'id': 'AHRQ_FRDOC_0001-0037', 'count': 1}],
                                                   [{'id': 'AHRQ_FRDOC_0002-0037', 'count': 2}]],
                                          'client_id': 'abcd', 'version': '0.5'})})
    assert len(rm.get_all_items_in_queue()) == 2
    assert rm.does_job_exist_in_progress('1234') is False


def test_docs_job_return_multiple_doc_place_in_db_queue_with_files(client):
    rm = RedisManager()
    with open(PATH + 'return_data.txt', 'r') as file:
        return_data = file.read().replace('\n', '')

    rm.add_to_queue(json.dumps({'data': ['Url1'], 'version': 'v0.5', 'type': 'docs', 'job_id': '1234'}))
    result = client.get('/get_work?client_id=asdf')
    
    assert {'data': ['Url1'], 'version': 'v0.5', 'type': 'docs', 'job_id': '1234'} == json.loads(result.data)
    assert rm.does_job_exist_in_progress('1234') is True

    client.post('/return_docs',
                data={'file': open(PATH + 'Archive.zip', 'rb'),
                      'json': json.dumps({'job_id': '1234', 'type': 'docs',
                                          'data': json.loads(return_data),
                                          'client_id': 'abcd', 'version': '0.5'})})
    assert len(rm.get_all_items_in_queue()) == 2
    assert rm.does_job_exist_in_progress('1234') is False


def test_docs_job_return_1000_doc_place_in_db_queue_with_helper_method(client):
    rm = RedisManager()

    return_data = return_data_ids(1000)

    rm.add_to_queue(json.dumps({'data': ['Url1'], 'version': 'v0.5', 'type': 'docs', 'job_id': '1234'}))
    result = client.get('/get_work?client_id=asdf')

    assert {'data': ['Url1'], 'version': 'v0.5', 'type': 'docs', 'job_id': '1234'} == json.loads(result.data)
    assert rm.does_job_exist_in_progress('1234') is True

    client.post('/return_docs',
                data={'file': open(PATH + 'Archive.zip', 'rb'),
                      'json': json.dumps({'job_id': '1234', 'type': 'docs',
                                          'data': json.loads(return_data),
                                          'client_id': 'abcd', 'version': '0.5'})})

    assert len(rm.get_all_items_in_queue()) == 1000
    assert rm.does_job_exist_in_progress('1234') is False


def test_docs_job_return_1000_doc_place_in_db_queue_with_helper_method_and_1000_archive(client):
    rm = RedisManager()

    return_data = return_data_ids(1000)

    rm.add_to_queue(json.dumps({'data': ['Url1'], 'version': 'v0.5', 'type': 'docs', 'job_id': '1234'}))
    result = client.get('/get_work?client_id=asdf')
    
    assert {'data': ['Url1'], 'version': 'v0.5', 'type': 'docs', 'job_id': '1234'} == json.loads(result.data)
    assert rm.does_job_exist_in_progress('1234') is True

    client.post('/return_docs',
                data={'file': open(PATH + 'Big_Archive.zip', 'rb'),
                      'json': json.dumps({'job_id': '1234', 'type': 'docs',
                                          'data': json.loads(return_data),
                                          'client_id': 'abcd', 'version': '0.5'})})

    assert len(rm.get_all_items_in_queue()) == 1000
    assert rm.does_job_exist_in_progress('1234') is False

@mock.patch('mirrulations_core.config.server_read_value', return_value=doc_path)
def test_doc_job_return_doc_saved(mock_dir, client):
    rm = RedisManager()
    rm.add_to_queue(
        json.dumps({"data": [{"id": "AAAA-AAAA-0001-0001", "count": 1}], "version": "v0.5", "type": "doc", "job_id": "1234"}))
    result = client.get('/get_work?client_id=asdf')

    client.post("/return_doc",
                data={'file': open(PATH + "test_single_doc.zip", 'rb'),
                      'json': json.dumps({'job_id': "1234", 'type': 'doc',
                                         'client_id': "abcd", "version": "0.5"})})
    assert len(rm.get_all_items_in_queue()) == 0
    count = get_count_of_doc()
    assert count == 1
    shutil.rmtree(config.server_read_value('regulations path'))
    assert rm.does_job_exist_in_progress('1234') is False

@mock.patch('mirrulations_core.config.server_read_value', return_value=doc_path)
def test_doc_job_return_two_doc_saved(mock_dir, client):
    rm = RedisManager()
    rm.add_to_queue(
        b'{"data": [{"id": "AAAA-AAAA-0001-0001", "count": 1}, {"id": "BBBB-BBBB-0001-0001", "count": 1}], "version": "v0.5", "type": "doc", "job_id": "1234"}')
    result = client.get('/get_work?client_id=asdf')

    client.post("/return_doc",
                data={'file': open(PATH + "test_two_doc.zip", 'rb'),
                      'json': json.dumps({'job_id': "1234", 'type': 'doc',
                                          'client_id': "abcd", "version": "0.5"})})
    count = get_count_of_doc()
    assert count == 2
    shutil.rmtree(config.server_read_value('regulations path'))
    assert len(rm.get_all_items_in_queue()) == 0
    assert rm.does_job_exist_in_progress('1234') is False

@mock.patch('mirrulations_core.config.server_read_value', return_value=doc_path)
def test_doc_job_return_100_doc_saved(mock_dir, client):
    rm = RedisManager()
    rm.add_to_queue(
        b'{"data": ["A"], "version": "v0.5", "type": "doc", "job_id": "1234"}')
    result = client.get('/get_work?client_id=asdf')

    client.post("/return_doc",
                data={'file': open(PATH + "test_100_doc.zip", 'rb'),
                      'json': json.dumps({'job_id': "1234", 'type': 'doc',
                                          'client_id': "abcd", "version": "0.5"})})
    count = get_count_of_doc()
    assert count == 100
    shutil.rmtree(config.server_read_value('regulations path'))
    assert len(rm.get_all_items_in_queue()) == 0
    assert rm.does_job_exist_in_progress('1234') is False

@mock.patch('mirrulations_core.config.server_read_value', return_value=doc_path)
def test_doc_job_return_1000_doc_saved(mock_dir, client):
    rm = RedisManager()
    rm.add_to_queue(
        b'{"data": ["A"], "version": "v0.5", "type": "doc", "job_id": "1234"}')
    result = client.get('/get_work?client_id=asdf')

    client.post("/return_doc",
                data={'file': open(PATH + "test_1000_doc.zip", 'rb'),
                      'json': json.dumps({'job_id': "1234", 'type': 'doc',
                                          'client_id': "abcd", "version": "0.5"})})
    count = get_count_of_doc()
    assert count == 1000
    shutil.rmtree(config.server_read_value('regulations path'))
    assert len(rm.get_all_items_in_queue()) == 0
    assert rm.does_job_exist_in_progress('1234') is False

@mock.patch('mirrulations_core.config.server_read_value', return_value=doc_path)
def test_doc_job_return_10000_doc_saved(mock_dir, client):
    rm = RedisManager()
    rm.add_to_queue(
        b'{"data": ["A"], "version": "v0.5", "type": "doc", "job_id": "1234"}')
    result = client.get('/get_work?client_id=asdf')

    client.post("/return_doc",
                data={'file': open(PATH + "test_10000_doc.zip", 'rb'),
                      'json': json.dumps({'job_id': "1234", 'type': 'doc',
                                          'client_id': "abcd", "version": "0.5"})})
    count = get_count_of_doc()

    assert count == 10000
    shutil.rmtree(config.server_read_value('regulations path'))
    assert len(rm.get_all_items_in_queue()) == 0
    assert rm.does_job_exist_in_progress('1234') is False

@mock.patch('mirrulations_core.config.server_read_value', return_value=doc_path)
def test_doc_job_return_10000_large_doc_saved(mock_dir, client):
    rm = RedisManager()
    rm.add_to_queue(
        b'{"data": ["A"], "version": "v0.5", "type": "doc", "job_id": "1234"}')
    result = client.get('/get_work?client_id=asdf')

    client.post("/return_doc",
                data={'file': open(PATH + "test_10000_doc_larger_json.zip", 'rb'),
                      'json': json.dumps({'job_id': "1234", 'type': 'doc',
                                          'client_id': "abcd", "version": "0.5"})})
    count = get_count_of_doc()

    assert count == 10000
    shutil.rmtree(config.server_read_value('regulations path'))
    assert len(rm.get_all_items_in_queue()) == 0
    assert rm.does_job_exist_in_progress('1234') is False