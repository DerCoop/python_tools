#!/usr/bin/env python

"""gawril is a smart tool to manipulate gpx files

* split one track into segments
* show gpx info

for short, it is an user API for gpxpy with some functionality which I needed
for my training
"""

__author__ = 'DerCoop'

import gpxpy
import collections


FilterData = collections.namedtuple(
    'FilterData',
    ('type', 'value'))


class Track:
    def __init__(self, input_fd):
        self.origin = gpxpy.parse(input_fd)
        input_fd.close()
        self.orig_points = []

    def convert_tp_to_list(self):
        """converts all points of the track to a list, do not take care of the segments etc"""
        for point in self.origin.walk(only_points=True):
            self.orig_points.append(point)

    def get_next_segment(self, filtertype, filtervalue):
        """document me"""
        import sys
        previous_point = self.get_next_point()
        point = self.get_next_point()
        time_from_start = 0

        if not point:
            print 'not enough points available'
            sys.exit(1)
        print point
        if filtertype == 't':
            while time_from_start <= filtervalue:
                time_from_start += time_difference(previous_point, point)
                print point
                previous_point = point
                point = self.get_next_point()

    def segment(self, filters):
        # give only one filter to operate on
        """split the track into different segments"""
        next_filter = filters.get_next_filter()
        while next_filter:
            self.get_next_segment(next_filter.type, next_filter.value)
            next_filter = filters.get_next_filter()

            """if previous_point: # and point_no > 0:
                if distance_2d:
                    distance = point.distance_2d(previous_point)
                else:
                    distance = point.distance_3d(previous_point)

                distance_from_start += distance
                time_from_start += point.time_difference(previous_point)
            else:
                starting_point = point


            #points.append(PointData(point, distance_from_start, track_no, segment_no, point_no))

            print 'Point at ({0},{1}) -> {2}, {3} at {4}m {5}s'.format(point.latitude, point.longitude,
                                                          point.elevation, point.time,
                                                          distance_from_start, time_from_start)
            previous_point = point
"""
        # TODO add the rest of the file to one last segment

    def get_next_point(self):
        try:
            return self.orig_points.pop(0)
        except IndexError as e:
            return None

    def print_track(self):
        for point in self.orig_points:
            print point


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


def split_track(origin, segments=None, filters=None):
    """split the track into segments, returns a new gpx object

    :segments - segment string
        segment: <type>:<value>
        type:   d - distance
                t - time
        value: integer value, for distance in meter, time in seconds

    :return
        segmented - the segmented gpx object
    """
    segmented = gpxpy.gpx.GPX()

    for track in origin.tracks:
        # Create track in the segmented GPX object:
        gpx_track = gpxpy.gpx.GPXTrack()
        segmented.tracks.append(gpx_track)
        # Create segment in the GPX track:
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)
        # get all points from the origin track, sorted
        # format: [trkpt:51.333190918,12.3977632523@-151.0@2015-01-12 17:42:53]
        for point in origin.walk(only_points=True):
            gpx_segment.points.append(point)

    return segmented


def print_track_info(gpx):
    """an interface to 'gpxinfo' from gpxpy"""
    from gawril.gpxinfo import print_gpx_info

    print_gpx_info(gpx)


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

    gawril(opts)
