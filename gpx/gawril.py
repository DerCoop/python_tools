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

def split_track(segments):
    """split the track into segments

    segments - segment string
        segment: <type>:<value>
        type:   d - distance
                t - time
        value: integer value, for distance in meter, time in seconds
    """
    pass


def print_track_info():
    """an interface to 'gpxinfo' from gppxpy"""
    pass


def gawril():
    pass


if __name__ == '__main__':
    gawril()