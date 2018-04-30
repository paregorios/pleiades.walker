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
