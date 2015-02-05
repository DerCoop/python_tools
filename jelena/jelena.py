#!/usr/bin/env python
from __future__ import print_function, absolute_import
"""jelena - comparator for PCAP files

Written by Der Coop <dercoop@users.sourceforge.net>

"""

import logging as log
import argparse


def get_cli_options():
    """returns a pair (values, args) of the command line options"""
    parser = argparse.ArgumentParser(description='Jelena - a tool to compare PCAP traces')
    # do not use filetype => the reader needs only the filename
    parser.add_argument('input_file', action='store', #type=argparse.FileType('r'),
                        nargs=2, help='the name of the input files to compare (=2!)')
    parser.add_argument('-O', '--output-file', action='store', #type=argparse.FileType('w'),
                        help='store the diff at a new PCAP file')
    parser.add_argument('-F', '--filter', action='store', default=None, nargs='*', metavar='FILTER',
                        choices=['src', 'src-ip', 'src-mac', 'dst', 'dst-ip', 'dst-mac',
                                 'mac', 'ip', 'seq-ack', 'ip-id', 'ttl', 'chksum', 'ttl',
                                 'ts', 'all'],
                        help='filter options, possible choices are: src src-ip src-mac dst dst-ip '
                             'dst-mac mac ip seq-ack ip-id ttl chksum ttl ts all')
    parser.add_argument('-L', '--loglevel', action='store', default='warning',
                        choices=['critical', 'error', 'warning', 'info', 'debug', 'notset'],
                        help='set your loglevel, default = warning')
    # TODO use the loglevel instead
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='print verbose')

    # TODO
    todo_config = parser.add_argument_group(title='ToDo',
                                            description='this arguments are not '
                                                        'completely implemented')
    todo_config.add_argument('-o', '--keep-order', action='store_true',
                             help='keep the incoming order of the pkg (untested)')

    return parser.parse_args()


def main():
    """the main function for jelena.py, the pcap compare tool

    this function is only needed for stand alone usage
    """
    args = get_cli_options()

    formatstring = '[%(levelname)s]: jelena: %(message)s'
    loglevel = log.getLevelName(args.loglevel.upper())

    # TODO write output to file
    log.basicConfig(format=formatstring, level=loglevel)

    # Parse pcap files
    dumps = []

    # Diff the dumps
    diff_packets = []

    # from left
    # pkgs are not sorted (input order)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        log.debug('abort by user')