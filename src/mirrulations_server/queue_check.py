import redis
from mirrulations_server.redis_manager import RedisManager


def queue_check(r):
    return r.get_all_items_in_progress_no_lock(), \
           r.get_all_items_in_queue_no_lock()


if __name__ == '__main__':
    r = RedisManager(redis.Redis())
    progress, queue = queue_check(r)
    print(progress)
    print(queue)
