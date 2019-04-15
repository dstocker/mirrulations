import random
import string
import redis
import mirrulations_core.api_call_management as api_manager
import mirrulations_server.redis_manager as redis_manager
import mirrulations_server.endpoints as endpoints
import mirrulations_core.config as config
from mirrulations_core.mirrulations_logging import logger


def monolith():
    """
    Runs the script. This is one monolithic function (aptly named)
    as the script just needs to be run; however, there is a certain
    point where I need to break out of the program if an error occurs,
    and I wasn't sure how exactly sys.exit() would work and whether
    or not it would mess with things outside of / calling this script,
    so I just made one giant method so I can return when needed.
    :return:
    """
    url_base = 'https://api.data.gov/regulations/v3/documents.json?rpp=1000'
    r = redis_manager.RedisManager(redis.Redis())
    regulations_key = config.server_read_value('api key')
    current_page = 0

    if regulations_key != '':
        # Gets number of documents available to download
        try:
            url = \
                'https://api.data.gov/regulations/v3/documents.json?api_key=' \
                + regulations_key + '&countsOnly=1'
            record_count = \
                api_manager.api_call_manager(url).json()['totalNumRecords']
        except api_manager.CallFailException:
            logger.error('Error occured with API request')
            print('Error occurred with docs_work_gen regulations API request.')
            return 0

        # Gets the max page we'll go to; each page is 1000 documents
        max_page_hit = record_count // 1000

        # This loop generates lists of URLs, sending out a job and
        # writing them to the work server every 1000 URLs.
        # It will stop and send whatever's left if we hit the max page limit.
        while current_page < max_page_hit:
            url_list = []
            for i in range(1000):
                current_page += 1
                url_full = url_base + '&po=' + str(current_page * 1000)

                url_list.append(url_full)

                if current_page == max_page_hit:
                    break

            # Makes a JSON from the list of URLs and send
            # it to the queue as a job
            docs_work = [''.join(
                random.choices(string.ascii_letters + string.digits, k=16)),
                'docs', url_list]
            r.add_to_queue(endpoints.generate_json(docs_work))
    else:
        print('No API Key!')


if __name__ == '__main__':
    monolith()
