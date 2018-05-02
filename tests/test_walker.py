#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test the place_crawler module."""

import logging
from nose.tools import assert_equal, assert_false, assert_is_none, assert_true, raises
from os.path import abspath, join, realpath
from pleiades.walker import Walker, JsonWalker, PlaceCollection, PleiadesWalker
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


class Test_Basics(TestCase):

    def setUp(self):
        """Setup steps to run before each place_crawler test."""
        global place_json_path
        self.place_json_path = abspath(realpath(join(*place_json_path)))

    def tearDown(self):
        """Change me"""
        pass

    @raises(IOError)
    def test_walker_bad_path(self):
        path = join('highway', 'to', 'hell')
        Walker(path=path)

    def test_walker_good_path(self):
        w = Walker(path=self.place_json_path)
        assert_false(w.count)
        assert_equal(len(w.extensions), 0)
        count, result = w.walk()
        assert_equal(count, 13)
        assert_is_none(result)

    def test_walker_no_count(self):
        w = Walker(path=self.place_json_path)
        count, result = w.walk(count=False)
        assert_false(count)

    def test_json_walker(self):
        w = JsonWalker(path=self.place_json_path)
        count, result = w.walk()


class Test_Indexing(TestCase):

    def setUp(self):
        """Setup steps to run before each place_crawler test."""
        global place_json_path
        self.place_json_path = abspath(realpath(join(*place_json_path)))
        w = PleiadesWalker(path=self.place_json_path)
        self.count, self.pc = w.walk()

    def tearDown(self):
        """Change me"""
        pass

    def test_pleiades_walker(self):
        assert_equal(self.count, 11)
        assert_equal(type(self.pc), PlaceCollection)

    def test_by_id(self):
        place = self.pc.get('id', '1000')[0]
        assert_equal(
            place.data['description'],
            'Germania Superior was a province of the Roman empire.')

    def test_by_name(self):
        places = self.pc.get('name', 'Actania')
        assert_equal(len(places), 1)
        assert_equal(places[0].data['id'], '101172')

    def test_pid_index(self):
        pids = sorted(list(self.pc.indices['id'].keys()))
        assert_equal(
            pids,
            ['1000', '101172', '200081', '200082', '200083', '200084',
                '200085', '200086', '200087', '200088', '200089'])

    def test_name_index(self):
        tokens = sorted(list(self.pc.indices['name'].keys()))
        assert_equal(['actania', 'germaniasuperior'], tokens)
