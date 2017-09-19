# -*- coding: utf-8 -*-

from opensky.core import OpenSkyMeasurer


def get_list_of_planes_near_goal(longitude=None, latitude=None, ordered=False):
    measurer = OpenSkyMeasurer(longitude=longitude, latitude=latitude)
    result = measurer.run(ordered=ordered)
    return result


if __name__ == '__main__':
    for row in get_list_of_planes_near_goal():
        print('callsign {callsign} longitude {longitude} latitude {latitude} '
              'distance to Paris {distance}'.format(**row))
