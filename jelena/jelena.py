#!/usr/bin/env python
from __future__ import print_function, absolute_import
"""jelena - comparator for PCAP files

Written by Der Coop <dercoop@users.sourceforge.net>

"""

import sys
import logging as log
import argparse
from scapy.all import wrpcap


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
    from lib.jelena import Jelena

    args = get_cli_options()

    formatstring = '[%(levelname)s]: jelena: %(message)s'
    loglevel = log.getLevelName(args.loglevel.upper())

    # TODO write output to file
    log.basicConfig(format=formatstring, level=loglevel)

    # Parse pcap files
    dumps = []

    for input_file in args.input_file:
        trace = Jelena(args.filter)
        dumps.append(trace.read_dump(input_file))

    # Diff the dumps
    diff_packets = []
    expected = dumps.pop(0)

    # from left
    # pkgs are not sorted (input order)
    for serial_packet, packet in expected.items():
        found_packet = False

        # for now we have only 2 files
        if args.keep_order:
            for dump in dumps:
                # XXX: with more than two files, ensure the right order of the files
                dump.pop(last=False)

        else:
            for dump in dumps:
                # TODO: go packet for packet through the dump
                if dump.get(serial_packet):
                    del dump[serial_packet]
                    found_packet = True

            if not found_packet:
                diff_packets.append(packet)
                log.debug('<<< %s' % packet.summary())

    # from right
    for dump in dumps:
        if len(dump) > 0:
            diff_packets.extend(dump.values())

            for packet in dump.values():
                log.debug('>>> %s' % packet.summary())

    log.debug('Found %s different packets' % str(len(diff_packets)))

    # Write pcap diff file?
    output_file = args.output_file

    if diff_packets:
        if output_file:
            log.info('write diff to file (%s)' % str(output_file))
            wrpcap(output_file, diff_packets)
        sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        log.debug('abort by user')