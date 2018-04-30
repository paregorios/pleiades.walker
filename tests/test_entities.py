#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test the place_crawler module."""

import json
import logging
from nose.tools import assert_equal, assert_false, assert_is_none, assert_true, raises
from os.path import abspath, join, realpath
from pleiades.walker import Place
from unittest import TestCase

logger = logging.getLogger(__name__)
test_data_path = ['tests', 'data']
place_json_path = test_data_path
place_json_path.append('place_json')


def setup_module():
    """Module-level setup steps for all place_crawler tests."""
    pass


def teardown_module():
    """Change me"""
    pass


class Test_Entities(TestCase):

    def setUp(self):
        """Setup steps to run before each place_crawler test."""
        global place_json_path
        self.place_json_path = abspath(realpath(join(*place_json_path)))

    def tearDown(self):
        """Change me"""
        pass

    @raises(KeyError)
    def test_untyped_constructor_attributes(self):
        d = {'some': 'junk'}
        Place(d)

    @raises(ValueError)
    def test_bad_place_type(self):
        d = {'@type': 'Knuckle'}
        Place(d)

    def test_place_load(self):
        fn = abspath(realpath(join(self.place_json_path, '1/0/1000.json')))
        with open(fn, 'r', encoding='utf-8') as f:
            j = json.load(f)
        del f
        p = Place(j)
        assert_equal(p.data['@type'], 'Place')
        assert_equal(
            sorted(list(p.data.keys())),
            sorted(
                ['@type', 'bbox', 'connectsWith', 'contributors', 'created',
                    'creators', 'description', 'details', 'features',
                    'history', 'id', 'locations', 'names', 'placeTypes',
                    'provenance', 'references', 'reprPoint', 'review_state',
                    'rights', 'subject', 'title', 'type', 'uri']))
