#!/usr/bin/env python

"""gawril is a smart tool to manipulate gpx files

* split one track into segments
* show gpx info

for short, it is an user API for gpxpy with some functionality which I needed
for my training
"""

__author__ = 'DerCoop'



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


def split_track(origin, segments=None):
    """split the track into segments, returns a new gpx object

    :segments - segment string
        segment: <type>:<value>
        type:   d - distance
                t - time
        value: integer value, for distance in meter, time in seconds

    :return
        segmented - the segmented gpx object
    """
    pass


def print_track_info(gpx):
    """an interface to 'gpxinfo' from gpxpy"""
    from lib.gpxinfo import print_gpx_info

    print_gpx_info(gpx)


def gawril():
    pass


if __name__ == '__main__':
    gawril()