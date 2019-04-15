import requests
import mirrulations_core.config as config
from mirrulations_core.mirrulations_logging import logger


def call(url):
    """
    Sends an API call to regulations.gov
    Raises exceptions if it is not a valid API call
    When a 300 status code is given, return a temporary
    exception so the user can retry the API call
    When a 429 status code is given, the user is out of
    API calls and must wait an hour to make more
    When 400 or 500 status codes are given there is
    a problem with the API connection
    :param url: the url that will be used to make the API call
    :return: returns the json format information of the documents
    """
    logger.warning('Making API call')
    result = requests.get(url)
    if 300 <= result.status_code < 400:
        logger.warning('API call failed')
        raise TemporaryException
    if result.status_code == 429:
        logger.warning('API call failed')
        raise ApiCountZeroException
    if 400 <= result.status_code < 600:
        logger.warning('API call failed')
        raise PermanentException
    logger.warning('API call successfully made')
    return result


def client_add_api_key(url):
    return url + '&api_key=' + config.client_read_value('api key')


def server_add_api_key(url):
    return url + '&api_key=' + config.server_read_value('api key')


class TemporaryException(Exception):
    """
    Raise an exception if there is an error communicating
    with either the work server or regulations
    """
    def __init__(self):
        logger.error('Error - Could not connect to API')


class ApiCountZeroException(Exception):
    """
    Raise an exception if the user is out of API calls
    """
    def __init__(self):
        logger.warning('API calls exhausted')


class PermanentException(Exception):
    """
    Raise an exception if there is an error with the API call
    """
    def __init__(self):
        logger.error('Error with the API call')
