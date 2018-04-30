#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 3 script template (changeme)
"""

import better_exceptions
from copy import deepcopy
import logging

logger = logging.getLogger(__name__)


class Place():

    def __init__(self, attributes: dict):
        try:
            e_type = attributes['@type']
        except KeyError:
            raise KeyError(
                'Attribute dictionary passed to Place constructor did not '
                'include a "@type" attribute: {}'.format(repr(attributes)))
        else:
            if e_type != 'Place':
                raise ValueError(
                    '"@type" attribute` passed to Place constructor had '
                    'unexpected value = "{}". Expected "Place".'
                    ''.format(e_type))
        self.data = deepcopy(attributes)


class PlaceCollection():

    def __init__(self, place_list=[]):
        self.places = []
        for place in place_list:
            self.add_place(place)

    def add_place(self, place):
        if isinstance(place, Place):
            self.places.append(place)
        elif isinstance(place, dict):
            self.places.append(Place(place))
        else:
            raise ValueError(
                'Unexpected argument type for PlaceCollection.add_place(): '
                '"{}". Expected "Place" or "dict".'.format(type(place)))
