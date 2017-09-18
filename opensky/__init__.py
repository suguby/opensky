# -*- coding: utf-8 -*-
import math
import requests


class OpenSkyMeasurerException(Exception):
    pass


class OpenSkyMeasurer:
    EARTH_RADIUS = 63727.95
    MIN_RADIUS = 400.0
    MAX_RADIUS = 500.0

    PARIS_LONGITUDE = 48.85341
    PARIS_LATITUDE = 2.3488

    def __init__(self, longitude=None, latitude=None):
        self._states = None
        self._near_to_target = []
        longitude = self.PARIS_LONGITUDE if longitude is None else longitude
        latitude = self.PARIS_LATITUDE if latitude is None else latitude
        latitude_rad = math.radians(latitude)
        self._goal_latitude_sin = math.sin(latitude_rad)
        self._goal_latitude_cos = math.cos(latitude_rad)
        self._goal_longitude_rad = math.radians(longitude)

    def run(self, ordered=False):
        self._get_data()
        self._proceed_data()
        if ordered:
            return sorted(self._near_to_target, key=lambda x: x['distance'])
        return self._near_to_target

    def _get_data(self):
        try:
            json_data = requests.get('https://opensky-network.org/api/states/all').json()
        except Exception as exc:
            # TODO more cases
            raise OpenSkyMeasurerException('No data from opensky-network.org. Exception is {}'.format(
                exc
            ))
        try:
            self._states = json_data['states']
        except KeyError:
            raise OpenSkyMeasurerException('Invalid data from opensky-network.org')

    def _proceed_data(self):
        self._near_to_target = []
        for state in self._states:
            if state[5] is None or state[6] is None:
                continue
            try:
                longitude, latitude = float(state[5]), float(state[6])
            except ValueError:
                continue
            distance = self._get_distance_to_goal(longitude=longitude, latitude=latitude)
            if self.MIN_RADIUS <= distance <= self.MAX_RADIUS:
                callsign = 'N/A' if state[0] is None else state[0]
                self._near_to_target.append(dict(
                    callsign=callsign,
                    longitude=longitude,
                    latitude=latitude,
                    distance=distance,
                ))

    def _get_distance_to_goal(self, longitude, latitude):
        # https://en.wikipedia.org/wiki/Great-circle_distance
        longitude_rad = math.radians(longitude)
        latitude_rad = math.radians(latitude)
        delta_longitude_rad = self._goal_longitude_rad - longitude_rad
        delta_rad = math.acos(
            self._goal_latitude_sin * math.sin(latitude_rad) +
            self._goal_latitude_cos * math.cos(latitude_rad) * math.cos(delta_longitude_rad)
        )
        distance = delta_rad * self.EARTH_RADIUS
        return distance


def get_list_of_planes_near_goal(longitude=None, latitude=None, ordered=False):
    measurer = OpenSkyMeasurer(longitude=longitude, latitude=latitude)
    result = measurer.run(ordered=ordered)
    return result


if __name__ == '__main__':
    for row in get_list_of_planes_near_goal():
        print('callsign {callsign} longitude {longitude} latitude {latitude} '
              'distance to Paris {distance}'.format(**row))
