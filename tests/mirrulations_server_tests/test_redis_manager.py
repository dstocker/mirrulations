import json
import mock
from mirrulations_server.redis_manager import RedisManager
from ast import literal_eval
import time


@mock.patch('mirrulations_server.redis_manager.reset_lock')
@mock.patch('mirrulations_server.redis_manager.set_lock')
def make_database(reset, lock):
    r = RedisManager()
    r.delete_all()
    list = json.dumps({"A": "a", "B": ["b", "c"]})
    list2 = json.dumps({"D": "d", "E": ["e", "f"]})
    list3 = json.dumps({"G": "g", "H": ["h", "i"]})
    r.add_to_queue(list)
    r.add_to_queue(list2)
    r.add_to_queue(list3)
    return r


def ignore_test_iterate():
    r = make_database()
    for item in r.get_all_items_in_queue():
        item = literal_eval(item.decode('utf-8'))
        if int(time.time()) - item[2] > 21600:
            print(int(time.time()) - item[2])
            print("Expired!")
        else:
            print(int(time.time()) - item[2])
            print("Still Good!")


def test_get_all_item_in_queue():
    r = make_database()
    items = r.get_all_items_in_queue()
    assert len(items) == 3


def test_get_all_item_in_progress():
    r = make_database()
    list4 = json.dumps(["l", ["m", "n"]])
    r.add_to_progress(list4)
    assert len(r.get_all_items_in_progress()) == 1


def test_get_work():
    r = make_database()
    assert len(r.get_all_items_in_queue()) == 3
    assert len(r.get_all_items_in_progress()) == 0
    work = r.get_work()
    assert work == {"A": "a", "B": ["b", "c"]}
    assert len(r.get_all_items_in_queue()) == 2
    assert len(r.get_all_items_in_progress()) == 1


def test_add_to_queue():
    r = make_database()
    list4 = json.dumps(["j", ["k", "l"]])
    assert len(r.get_all_items_in_queue()) == 3
    r.add_to_queue(list4)
    assert len(r.get_all_items_in_queue()) == 4


def test_delete_all():
    r = make_database()
    r.delete_all()
    assert len(r.get_all_items_in_queue()) == 0
    assert len(r.get_all_items_in_progress()) == 0


@mock.patch('mirrulations_server.redis_manager.get_curr_time',
            return_value=1531911498)
def test_find_expired(time):  # time):
    r = make_database()
    r.delete_all()
    t3 = json.dumps((["g", ["h", "i"]]))
    r.add_to_progress(t3)
    assert len(r.get_all_items_in_progress()) == 1
    r.find_expired()
    assert len(r.get_all_items_in_progress()) == 0


def test_find_no_expired():
    r = make_database()
    r.delete_all()
    t3 = json.dumps((["g", ["h", "i"]]))
    t2 = json.dumps((["j", ["k", "l"]]))
    r.add_to_progress(t3)
    r.add_to_progress(t2)
    assert len(r.get_all_items_in_progress()) == 2
    r.find_expired()
    assert len(r.get_all_items_in_progress()) == 2


def test_get_specific_item_from_queue():
    r = make_database()
    r.delete_all()
    r.add_to_queue(json.dumps({"A": "B", "job_id": "d"}))
    assert r.get_specific_job_from_queue("d") == json.dumps({
        "A": "B", "job_id": "d"})


def test_get_specific_item_from_queue_does_not_match():
    r = make_database()
    r.delete_all()
    r.add_to_queue(json.dumps({"A": "B", "job_id": "c"}))
    assert r.get_specific_job_from_queue(
        "d") == '{"job_id":"null", "type":"none"}'


def test_remove_specific_job_from_queue():
    r = make_database()
    r.delete_all()
    r.add_to_queue(json.dumps({"A": "B", "job_id": "c"}))
    r.add_to_queue(json.dumps({"A": "B", "job_id": "d"}))
    assert len(r.get_all_items_in_queue()) == 2
    r.remove_specific_job_from_queue("c")
    assert len(r.get_all_items_in_queue()) == 1
    r.remove_specific_job_from_queue("d")
    assert len(r.get_all_items_in_queue()) == 0


def test_remove_specific_job_from_queue_no_item():
    r = make_database()
    r.delete_all()
    r.add_to_queue(json.dumps({"A": "B", "job_id": "c"}))
    r.add_to_queue(json.dumps({"A": "B", "job_id": "d"}))
    assert len(r.get_all_items_in_queue()) == 2
    r.remove_specific_job_from_queue("a")
    assert len(r.get_all_items_in_queue()) == 2


@mock.patch('mirrulations_server.redis_manager.get_curr_time', return_value=15)
def test_get_keys_progress(time):
    r = make_database()
    r.delete_all()
    r.add_to_progress(json.dumps({"A": "B", "job_id": "c"}))
    r.add_to_progress(json.dumps({"A": "B", "job_id": "d"}))
    assert r.get_keys_from_progress("d") == "15"


@mock.patch('mirrulations_server.redis_manager.get_curr_time', return_value=15)
def test_does_job_exist_in_progress(time):
    r = make_database()
    r.delete_all()
    r.add_to_progress(json.dumps({"A": "B", "job_id": "c"}))
    assert r.does_job_exist_in_progress("c")


@mock.patch('mirrulations_server.redis_manager.get_curr_time', return_value=15)
def test_delete_from_progress(time):
    r = make_database()
    r.delete_all()
    r.add_to_progress(json.dumps({"A": "B", "job_id": "c"}))
    assert len(r.get_all_items_in_progress()) == 1
    r.remove_job_from_progress(15)
    assert len(r.get_all_items_in_progress()) == 0


@mock.patch('mirrulations_server.redis_manager.get_curr_time', return_value=15)
def test_renew_job(time):
    r = make_database()
    r.delete_all()
    r.add_to_progress(json.dumps({"A": "B", "job_id": "c"}))
    assert len(r.get_all_items_in_progress()) == 1
    assert len(r.get_all_items_in_queue()) == 0
    r.renew_job("c")
    assert len(r.get_all_items_in_queue()) == 1
    assert len(r.get_all_items_in_progress()) == 0
