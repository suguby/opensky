# -*- coding: utf-8 -*-
import json
import unittest
from unittest import mock

import os

from opensky import OpenSkyMeasurer


class TestOpenSkyMeasurer(unittest.TestCase):

    def setUp(self):
        fixture_path = os.path.join(os.path.dirname(__file__), 'fixture.json')
        with open(fixture_path, 'r') as fp:
            test_data = json.load(fp)
        OpenSkyMeasurer._get_data = mock.Mock(
            return_value=test_data
        )

    def test_functional(self):
        measurer = OpenSkyMeasurer(longitude=44.0, latitude=55.0)
        result = measurer.run(min_radius=800, max_radius=900)
        self.assertEqual(len(result), 1)
        stat = result[0]
        self.assertEqual(stat['callsign'], '7800ee')
        self.assertEqual(stat['longitude'], 45.2549)
        self.assertEqual(stat['latitude'], 55.1871)
        self.assertEqual(stat['distance'], 825.3702658367322)
