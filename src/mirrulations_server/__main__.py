import argparse
import os
from redis import Redis
from threading import Thread

from mirrulations_core.config import SERVER_CONFIG_FILE, server_config_setup

from mirrulations_server.docs_work_gen import monolith
from mirrulations_server.endpoints import run
from mirrulations_server.expire import expire


def parse_args():
    parser = argparse.ArgumentParser(prog='mirrulations_server')
    parser.add_argument('-c', '--config',
                        action='store_true',
                        help='force config setup')
    return vars(parser.parse_args())


def main():
    args = parse_args()
    if args['config'] or not os.path.exists(SERVER_CONFIG_FILE):
        server_config_setup()

    if Redis().ping() != 'PONG':
        print('Run redis-server before running mirrulations_server!')
        exit()

    def run_flask():
        run()

    def run_work():
        monolith()
        expire()

    Thread(target=run_flask).start()
    Thread(target=run_work).start()
