#/usr/bin/env python

"""gawril is a smart tool to manipulate gpx files

* split one track into segments
* show gpx info

for short, it is an user API for gpxpy with some functionality which I needed
for my training
"""

__author__ = 'DerCoop'


def parse_clo():
    """parse the command line options"""
    pass


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