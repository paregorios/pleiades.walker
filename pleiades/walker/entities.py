#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 3 script template (changeme)
"""

import better_exceptions
from copy import deepcopy
import logging
import unicodedata
import unidecode
import sys

logger = logging.getLogger(__name__)
punct_table = dict.fromkeys(
    i for i in range(sys.maxunicode)
    if unicodedata.category(chr(i)).startswith('P'))


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
        self.indices = {}
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
        index_titles = ['id', 'name']
        for it in index_titles:
            try:
                self.indices[it]
            except KeyError:
                self.indices[it] = {}
            finally:
                self._index(it, self.places[-1])

    def _index(self, it, place):
        logger.debug('index {}'.format(it))
        index = self.indices[it]
        if it == 'id':
            index[place.data['id']] = place
            logger.debug(index)
        else:
            getattr(self, '_do_index_{}'.format(it))(place)

    def _do_index_name(self, place):
        index = self.indices['name']
        tokens = place.data['title'].split('/')
        for name in place.data['names']:
            tokens.append(name['attested'])
            tokens.extend(name['romanized'].split(','))
        tokens = [t.strip() for t in tokens if t.strip() != '']
        tokens = [self._tokenize(t) for t in tokens]
        tokens = list(set(tokens))
        tokens = [t for t in tokens if not (
            t.startswith('untitled') or t.startswith('unnamed'))]
        for token in tokens:
            try:
                entry = index[token]
            except KeyError:
                index[token] = []
                entry = index[token]
            finally:
                entry.append(place.data['id'])

    def _get_index_name(self, value):
        name_index = self.indices['name']
        pid_index = self.indices['id']
        token = self._tokenize(value)
        return [pid_index[pid] for pid in name_index[token]]

    def _tokenize(self, raw: str):
        cooked = raw.strip()
        cooked = cooked.translate(punct_table)
        cooked = unidecode.unidecode(cooked)
        cooked = ''.join(cooked.split()).lower()
        return cooked

    def get(self, it, value):
        if it == 'id':
            return [self.indices['id'][value]]
        else:
            return getattr(self, '_get_index_{}'.format(it))(value)

    def __add__(self, *args):
        if len(args) == 0:
            return deepcopy(self)
        else:
            result = deepcopy(self)
            for pc in args:
                for p in pc.places:
                    result.add_place(p)
        return result
