import argparse
import os

from mirrulations_core.config import CLIENT_CONFIG_FILE, client_config_setup

from mirrulations_client.client import do_work


def parse_args():
    parser = argparse.ArgumentParser(prog='mirrulations_client')
    parser.add_argument('-c', '--config',
                        action='store_true',
                        help='force config setup')
    return vars(parser.parse_args())


def main():
    args = parse_args()
    if args['config'] or not os.path.exists(CLIENT_CONFIG_FILE):
        client_config_setup()

    do_work()
