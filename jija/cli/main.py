import os
import argparse
import sys

from jija.cli.base import CliCommand
from jija.cli.commands import COMMANDS


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--settings', nargs='?', default='settings.py', help='settings.py file')
    subparsers = parser.add_subparsers(title='commands', required=True)

    for name, command in COMMANDS.items():
        command_parser = subparsers.add_parser(name, prog=name)
        command.fill_parser(command_parser)

    return parser


def main():
    args = ['jija', 'create-app'][1:]
    args = []
    # args = []

    # args = sys.argv[:1]
    len(args) == 0 and args.append('-h')

    parser = create_parser()
    print(parser.parse_args(args))
    # print(command)

    # print(os.getcwd())
    # print('hello from cli')



if __name__ == '__main__':
    main()
