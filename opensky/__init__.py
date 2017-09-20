# -*- coding: utf-8 -*-

from opensky.core import OpenSkyMeasurer


def get_list_of_planes_near_goal(longitude=None, latitude=None, min_radius=None, max_radius=None, ordered=False):
    measurer = OpenSkyMeasurer(longitude=longitude, latitude=latitude)
    result = measurer.run(min_radius=min_radius, max_radius=max_radius, ordered=ordered)
    return result


if __name__ == '__main__':
    for row in get_list_of_planes_near_goal(
            # longitude=51.1837, latitude=24.8133,
            min_radius=0, max_radius=5000, ordered=True):
        print('callsign {callsign} longitude {longitude} latitude {latitude} '
              'distance to goal {distance}'.format(**row))
