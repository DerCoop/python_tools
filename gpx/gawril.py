#!/usr/bin/env python

"""gawril is a smart tool to manipulate gpx files

* split one track into segments
* show gpx info

for short, it is an user API for gpxpy with some functionality which I needed
for my training
"""

__author__ = 'DerCoop'

import collections
import sys

try:
    import gpxpy
except ImportError as e:
    print('Import Error (%s)' % e)
    print('try "sudo pip install gpxpy" to install gpxpy')
    sys.exit(1)


FilterData = collections.namedtuple(
    'FilterData',
    ('type', 'value'))


            previous_point = point




class SegmentFilter:
    def __init__(self, filterstrings):
        self.filter = []
        self.parse_filterstring(filterstrings)

    def parse_filterstring(self, filterstrings):
        """splits the filter string
            1 - split the comma separated list into single filterstrings (one string for each filter)
            2 - split each filterstring (type:value - pair) into type and value and store it in a collection list
            """
        if not filterstrings:
            return
        for filterstring in filterstrings.split(','):
            try:
                f_type, value = filterstring.split(':')
            except ValueError as e:
                # ignore invalid filters
                # TODO print a warning
                pass
            else:
                self.filter.append(FilterData(f_type, value))

    def get_next_filter(self):
        """returns the filter from the front of the list and remove it from list, None if the list is empty"""
        try:
            return self.filter.pop(0)
        except IndexError as e:
            return None


def get_cli_options():
    """returns a pair (values, args) of the command line options"""
    import argparse
    parser = argparse.ArgumentParser(description='gawril - manipulate your gpx files')
    parser.add_argument('-I', '--input-file', action='store', type=argparse.FileType('r'),
                        required=True,
                        help='the gpx source file')
    parser.add_argument('-S', '--segments', action='store',
                        help='defined segments, comma separated list with the format: '
                             '(type:value,type:value)')
    parser.add_argument('-2', '--2D', action='store_true',
                        help='use only 2 dimensions')


    # TODO
    todo_config = parser.add_argument_group(title='ToDo',
                                            description='this arguments are not '
                                                        'completely implemented')
    todo_config.add_argument('-O', '--store-output', action='store', type=argparse.FileType('w'),
                             help='the name of the file where the output should be stored')
    todo_config.add_argument('-L', '--loglevel', action='store', default='warning',
                        choices=['critical', 'error', 'warning', 'info', 'debug', 'notset'],
                        help='set your loglevel, default = warning')
    todo_config.add_argument('-v', '--verbose', action='store_true',
                        help='print verbose')

    return parser.parse_args()


def gawril(opts):
    gpx_fd = gpxpy.parse(opts.input_file)
    opts.input_file.close()

    filters = SegmentFilter(opts.segments)

    segmented = split_track(gpx_fd, filters)

    if opts.verbose:
        print_track_info(gpx_fd)
        print_track_info(segmented)

    if opts.store_output:
        print('write output to "%s"' % opts.store_output.name)
        opts.store_output.write(segmented.to_xml())
        opts.store_output.close()


if __name__ == '__main__':
    opts = get_cli_options()


