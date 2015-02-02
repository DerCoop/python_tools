#!/usr/bin/env python
from __future__ import print_function

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


class Gawril(object):
    """main class for gavril"""
    def __init__(self, source_fd):
        self.origin = gpxpy.parse(source_fd)
        source_fd.close()

    def print_track(self, track=None):
        """print information of the origin track, an interface to 'gpxinfo' from gpxpy"""
        from gawril.gpxinfo import print_gpx_info

        if not track:
            print_gpx_info(self.origin)
        else:
            print_gpx_info(track)

    def split_track(self, segments=None, filters=None):
        """split the track into segments, returns a new gpx object

        :param segments: - segment string
            segment: <type>:<value>
            type:   d - distance
                    t - time
            value: integer value, for distance in meter, time in seconds

        :return:
            segmented - the segmented gpx object
        """
        # create a list of segments
        segmented_gpx = gpxpy.gpx.GPX()
        # Create track in the segmented GPX object:
        gpx_track = gpxpy.gpx.GPXTrack()
        segmented_gpx.tracks.append(gpx_track)

        dist_diff = 0
        time_diff = 0
        previous_point = None

        flt = filters.get_next_filter()
        print(flt)
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)
        for point in self.origin.walk(only_points=True):
            if previous_point:
                time_diff += point.time_difference(previous_point)
                dist_diff += point.distance_2d(previous_point)
            if not check_filter(dist_diff, time_diff, flt):
                flt = filters.get_next_filter()
                gpx_segment = gpxpy.gpx.GPXTrackSegment()
                gpx_track.segments.append(gpx_segment)
                dist_diff = 0
                time_diff = 0
            gpx_segment.points.append(point)
            previous_point = point

        return segmented_gpx


def check_filter(dist_diff, time_diff, flt):
    """check if the filter limit is exceeded"""
    # TODO make it dict
    if not flt:
        return True
    if flt.type == 't' and int(time_diff) <= int(flt.value):
            return True
    if flt.type == 'd' and int(dist_diff) <= int(flt.value):
        return True
    return False


class SegmentFilter:
    def __init__(self, filterstrings):
        self.filter = list()
        self.parse_filterstring(filterstrings)

    def parse_filterstring(self, filterstrings):
        """splits the filter string
            1 - split the comma separated list into single filterstrings (one string for each filter)
            2 - split each filterstring (type:value - pair)
                    into type and value and store it in a collection list

            TODO add doctest

        :param filterstrings:
            the filterstring to split into (filtertype, value)
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
        """returns the filter from the front of the list and remove it from list

        :return:
            the next filter Tuple(type, value), None if the list is empty
        """
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
    trk = Gawril(opts.input_file)

    filters = SegmentFilter(opts.segments)

    segmented = trk.split_track(filters=filters)

    if opts.verbose:
        trk.print_track()
        trk.print_track(segmented)

    if opts.store_output:
        print('write output to "%s"' % opts.store_output.name)
        opts.store_output.write(segmented.to_xml())
        opts.store_output.close()


if __name__ == '__main__':
    opts = get_cli_options()

    gawril(opts)

# TODO add some tests with the testtracks (do not use only my own/local tracks,
# use skiing tracks or TransX)
