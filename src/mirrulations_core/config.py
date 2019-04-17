from configparser import ConfigParser
import os
import random
import requests
import string

from mirrulations_core.mirrulations_logging import logger

CONFIG_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                          '../../.config/')
CLIENT_CONFIG_FILE = CONFIG_DIR + 'client.ini'
SERVER_CONFIG_FILE = CONFIG_DIR + 'server.ini'
WEB_CONFIG_FILE = CONFIG_DIR + 'web.ini'

connection_error_string = 'Unable to connect!\n' \
                          'We weren\'t able to connect to regulations.gov.\n' \
                          'Please try again later.'
invalid_key_error_string = 'Invalid API key!\n' \
                           'Your API key is invalid.\n' \
                           'Please visit\n' \
                           'https://regulationsgov.github.io/developers/\n' \
                           'for an API key.'
successful_login_string = 'Success!\n' \
                          'You are successfully logged in.'


def read_value(value, string, config_path):
    """
    Reads a file from the configuration JSON file.
    :param value: Value to be read from the JSON
    :return: Value read from the JSON
    """

    try:
        config = ConfigParser()
        config.read(config_path)
        result = config[string][value]
    except FileNotFoundError:
        logger.error('Error - File Not Found')
        return None
    except IOError:
        logger.error('Error - Invalid Input/Output')
        return None
    except KeyError:
        logger.error('API Key Error')
        return None
    else:
        return result


def client_read_value(value):
    return read_value(value, 'CLIENT', CLIENT_CONFIG_FILE)


def server_read_value(value):
    return read_value(value, 'SERVER', SERVER_CONFIG_FILE)


def web_read_value(value):
    return read_value(value, 'WEB', WEB_CONFIG_FILE)


def verify_api_key(api_key):
    try:
        r = requests.get('https://api.data.gov/regulations/v3/documents.json'
                         '?api_key=' + api_key)
    except requests.ConnectionError:
        print(connection_error_string)
        exit()
    else:
        if r.status_code == 403:
            print(invalid_key_error_string)
            exit()
        elif r.status_code > 299 and r.status_code != 429:
            print(connection_error_string)
            exit()
        print(successful_login_string)


def client_config_setup():

    api_key = input('API Key:\n')
    verify_api_key(api_key)

    client_id = ''.join(random.choices(string.ascii_letters + string.digits,
                                       k=16))
    ip = input('IP:\n')
    port = input('Port:\n')

    if not os.path.exists(CONFIG_DIR):
        os.mkdir(CONFIG_DIR)

    with open(CLIENT_CONFIG_FILE, 'wt') as file:
        config = ConfigParser()
        config['CLIENT'] = {
            'api key': api_key,
            'client id': client_id,
            'ip': ip,
            'port': port
        }
        config.write(file)
        file.close()


def server_config_setup():

    api_key = input('API Key:\n')
    verify_api_key(api_key)

    regulations_path = input('Location to save Documents:\n')
    if not regulations_path.endswith('/'):
        regulations_path = regulations_path + '/'

    client_path = input('Location to save Client Logs:\n')
    if not client_path.endswith('/'):
        client_path = client_path + '/'

    if not os.path.exists(CONFIG_DIR):
        os.mkdir(CONFIG_DIR)

    with open(SERVER_CONFIG_FILE, 'wt') as file:
        config = ConfigParser()
        config['SERVER'] = {
            'api key': api_key,
            'regulations path': regulations_path,
            'client path': client_path
        }
        config.write(file)
        file.close()


def web_config_setup():

    regulations_path = input('Location to save Documents:\n')
    if not regulations_path.endswith('/'):
        regulations_path = regulations_path + '/'

    if not os.path.exists(CONFIG_DIR):
        os.mkdir(CONFIG_DIR)

    with open(WEB_CONFIG_FILE, 'wt') as file:
        config = ConfigParser()
        config['WEB'] = {
            'regulations path': regulations_path
        }
        config.write(file)
        file.close()
