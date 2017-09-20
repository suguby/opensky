# -*- coding: utf-8 -*-
import math

import requests

from opensky.exceptions import OpenSkyMeasurerException


class OpenSkyMeasurer:
    EARTH_RADIUS = 6371.0
    MIN_RADIUS = 400.0
    MAX_RADIUS = 500.0

    PARIS_LONGITUDE = 48.85341
    PARIS_LATITUDE = 2.3488

    def __init__(self, longitude=None, latitude=None):
        self._states = None
        self._near_to_target = []
        self._goal_longitude = self.PARIS_LONGITUDE if longitude is None else longitude
        self._goal_longitude_rad = math.radians(self._goal_longitude)
        self._goal_latitude = self.PARIS_LATITUDE if latitude is None else latitude
        self._goal_latitude_rad = math.radians(self._goal_latitude)
        self._goal_latitude_sin = math.sin(self._goal_latitude_rad)
        self._goal_latitude_cos = math.cos(self._goal_latitude_rad)
        self.min_radius = None
        self.max_radius = None
        self.goal_bond_degrees = None

    def run(self, min_radius=None, max_radius=None, ordered=False):
        self.min_radius = self.MIN_RADIUS if min_radius is None else min_radius
        self.max_radius = self.MAX_RADIUS if max_radius is None else max_radius
        # один угловой градус ~111 км на поверхности, проверять будет только те борта,
        # которые попали в квадрат с границами self.goal_bond_degrees
        self.goal_bond_degrees = round(self.max_radius / 111.0)
        self._states = self._get_data()
        self._near_to_target = self._proceed_data()
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
            return json_data['states']
        except KeyError:
            raise OpenSkyMeasurerException('Invalid data from opensky-network.org')

    def _proceed_data(self):
        result = []
        for state in self._states:
            callsign = 'N/A' if state[1] is None else state[1].strip()
            if state[5] is None or state[6] is None:
                continue
            try:
                longitude, latitude = float(state[5]), float(state[6])
            except ValueError:
                continue
            if abs(self._goal_longitude - longitude) > self.goal_bond_degrees \
                    or abs(self._goal_latitude - latitude) > self.goal_bond_degrees:
                continue
            distance = self._get_distance_to_goal(longitude=longitude, latitude=latitude)
            if self.min_radius <= distance <= self.max_radius:
                result.append(dict(
                    callsign=callsign,
                    longitude=longitude,
                    latitude=latitude,
                    distance=distance,
                ))
        return result

    def _get_distance_to_goal(self, longitude, latitude):
        # широта и долгота - latitude and longitude
        # https://en.wikipedia.org/wiki/Great-circle_distance
        longitude_rad = math.radians(longitude)
        latitude_rad = math.radians(latitude)

        delta_longitude_rad = self._goal_longitude_rad - longitude_rad
        delta_rad = math.acos(
            self._goal_latitude_sin * math.sin(latitude_rad) +
            self._goal_latitude_cos * math.cos(latitude_rad) * math.cos(delta_longitude_rad)
        )

        # delta_rad_2 = 2 * math.asin(math.sqrt(
        #     math.sin((latitude_rad - self._goal_latitude_rad) / 2.0) ** 2
        #     + math.cos(latitude_rad) * math.cos(self._goal_latitude_rad) * math.sin(
        #         (longitude_rad - self._goal_longitude_rad) / 2.0
        #     ) ** 2
        # ))
        distance = delta_rad * self.EARTH_RADIUS
        return distance