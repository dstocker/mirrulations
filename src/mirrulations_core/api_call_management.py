import time
from mirrulations_core.api_call import call,\
                                       ApiCountZeroException,\
                                       PermanentException,\
                                       TemporaryException
from mirrulations_core.mirrulations_logging import logger


def api_call_manager(url):
    """
    If there were no errors in making an API call, get the result
    If a Temporary error occurred, sleep for 5 minutes and try again.
    Do this 50 times, and if it continues to fail, raise a CallFailException
    If a Permanent error occurs, raise a CallFailException
    If the user's ApiCount is zero, sleep for one hour to refresh the calls
    :param url: the url that will be used to make the API call
    :return: returns the resulting information of the documents
    """

    pause = 0
    while pause < 51:
        try:
            result = call(url)
            return result
        except TemporaryException:
            logger.error('API call Error, waiting 5 minutes')
            time.sleep(300)
            pause += 1
        except PermanentException:
            logger.error('API call Error')
            break
        except ApiCountZeroException:
            logger.warning('API calls exhausted')
            time.sleep(3600)
    logger.error('API call failed')
    raise CallFailException


class CallFailException(Exception):
    """
    Raise an exception is there is an error making the API call
    """
    def __init__(self):
        logger.error('Error - API call failed')
