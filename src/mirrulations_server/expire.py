import redis
from mirrulations_server.redis_manager import RedisManager
import time


def expire():
    """
    Checks to see if any of the in-progress jobs have expired
    :return:
    """
    while True:
        RedisManager(redis.Redis()).find_expired()
        time.sleep(3600)


if __name__ == '__main__':
    expire()
