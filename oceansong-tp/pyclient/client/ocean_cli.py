import argparse
import getpass
import logging
import os
import sys
import traceback
import pkg_resources

from colorlog import ColoredFormatter

from client.ocean_client import OceanClient

DISTRIBUTION_NAME = 'simplewallet'

DEFAULT_URL = 'http://localhost:8008'

def create_console_handler(verbose_level):
    clog = logging.StreamHandler()
    formatter = ColoredFormatter(
        "%(log_color)s[%(asctime)s %(levelname)-8s%(module)s]%(reset)s "
        "%(white)s%(message)s",
        datefmt="%H:%M:%S",
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red',
        })

    clog.setFormatter(formatter)
    clog.setLevel(logging.DEBUG)
    return clog

def setup_loggers(verbose_level):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(create_console_handler(verbose_level))

def add_register_parser(subparsers, parent_parser):
    '''Define the "register" command line parsing.'''
    parser = subparsers.add_parser(
        'register',
        help='register new IoT device',
        parents=[parent_parser])

    parser.add_argument(
        'deviceID',
        type=int,
        help='the ID of IoT device to register')

    parser.add_argument(
        'gatewayKey',
        type=str,
        help='the Key of gateway of this device')

def create_parent_parser(prog_name):
    '''Define the -V/--version command line options.'''
    parent_parser = argparse.ArgumentParser(prog=prog_name, add_help=False)

    try:
        version = pkg_resources.get_distribution(DISTRIBUTION_NAME).version
    except pkg_resources.DistributionNotFound:
        version = 'UNKNOWN'

    parent_parser.add_argument(
        '-V', '--version',
        action='version',
        version=(DISTRIBUTION_NAME + ' (Hyperledger Sawtooth) version {}')
        .format(version),
        help='display version information')

    return parent_parser


def create_parser(prog_name):
    '''Define the command line parsing for all the options and subcommands.'''
    parent_parser = create_parent_parser(prog_name)

    parser = argparse.ArgumentParser(
        description='Provides subcommands to manage your simple wallet',
        parents=[parent_parser])

    subparsers = parser.add_subparsers(title='subcommands', dest='command')

    subparsers.required = True

    add_register_parser(subparsers, parent_parser)

    return parser

def _get_keyfile(customerName):
    '''Get the private key for a customer.'''
    home = os.path.expanduser("~")
    key_dir = os.path.join(home, ".sawtooth", "keys")

    return '{}/{}.priv'.format(key_dir, customerName)

def _get_pubkeyfile(customerName):
    '''Get the public key for a customer.'''
    home = os.path.expanduser("~")
    key_dir = os.path.join(home, ".sawtooth", "keys")

    return '{}/{}.pub'.format(key_dir, customerName)

def do_register(args):
    '''Implements the "register" subcommand by calling the client class.'''
    keyfile = _get_keyfile(args.gatewayKey)

    client = OceanClient(baseUrl=DEFAULT_URL, keyFile=keyfile)

    response = client.register(args.deviceID)

    print("Response: {}".format(response))

def main(prog_name=os.path.basename(sys.argv[0]), args=None):
    '''Entry point function for the client CLI.'''
    if args is None:
        args = sys.argv[1:]
    parser = create_parser(prog_name)
    args = parser.parse_args(args)

    verbose_level = 0

    setup_loggers(verbose_level=verbose_level)

    # Get the commands from cli args and call corresponding handlers
    if args.command == 'register':
        do_register(args)
    else:
        raise Exception("Invalid command: {}".format(args.command))


def main_wrapper():
    try:
        main()
    except KeyboardInterrupt:
        pass
    except SystemExit as err:
        raise err
    except BaseException as err:
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

