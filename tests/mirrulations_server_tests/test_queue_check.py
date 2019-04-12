import fakeredis
import json
from mirrulations_server.queue_check import queue_check
from mirrulations_server.redis_manager import RedisManager


def emptydatabase():
    r = RedisManager(fakeredis.FakeRedis())
    return r


def make_database():
    r = RedisManager(fakeredis.FakeRedis())
    r.delete_all()
    list = json.dumps({"A": "a", "B": ["b", "c"]})
    list2 = json.dumps({"D": "d", "E": ["e", "f"]})
    list3 = json.dumps({"G": "g", "H": ["h", "i"]})
    r.add_to_queue(list)
    r.add_to_queue(list2)
    r.add_to_progress(list3)
    return r


def test_queue_check_empty():
    r = emptydatabase()
    a, b = queue_check(r)
    assert len(a) == 0
    assert len(b) == 0


def test_queue_check_items_in_queue():
    r = make_database()
    a, b = queue_check(r)
    assert len(a) == 1
    assert len(b) == 2
