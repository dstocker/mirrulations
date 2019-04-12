import random
import string
import redis
import mirrulations_server.redis_manager as redis_manager
import mirrulations_server.endpoints as endpoints

redis.Redis().flushdb()

r = redis_manager.RedisManager(redis.Redis())

docs_work = [''.join(random.choice(string.ascii_uppercase + string.digits)
                     for _ in range(16)), "docs",
             ['https://api.data.gov/regulations/v3/'
              'documents.json?rpp=1000&po=11268000']]

r.add_to_queue(endpoints.generate_json(docs_work))
