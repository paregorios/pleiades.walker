#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 3 script template (changeme)
"""

import better_exceptions
from copy import deepcopy
import dateutil.parser
import logging
from pprint import pformat
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
        self.data = attributes

    def __str__(self):
        return """https://pleiades.stoa.org/places/{id}
{title}
{description}
""".format(**self.data)


class PlaceCollection():

    def __init__(self, place_list=[]):
        self.places = []
        self.indices = {
            'id': {},
            'name': {},
            'modified': {},
            'words': {}
        }
        self.most_recent = '19700101'
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
        index_titles = [k for k in self.indices.keys() if k != 'words']
        for it in index_titles:
            self._index(it, self.places[-1])

    def _index(self, it, place=None):
        # logger.debug('index {}'.format(it))
        index = self.indices[it]
        if it == 'id':
            index[place.data['id']] = place
            # logger.debug(index)
        else:
            if place is not None:
                getattr(self, '_do_index_{}'.format(it))(place)
            else:
                getattr(self, '_do_index_{}'.format(it))()

    def _do_index_name(self, place):
        index = self.indices['name']
        names = place.data['title'].split('/')
        for name in place.data['names']:
            if name['attested'] is not None:
                names.append(name['attested'])
            names.extend(name['romanized'].split(','))
        names = [n.strip() for n in names if n is not None and n.strip() != '']
        tokens = [self._tokenize(n) for n in names]
        tokens = list(set(tokens))
        tokens = [t for t in tokens if not (
            t.startswith('untitled') or t.startswith('unnamed'))]
        pid = place.data['id']
        for token in tokens:
            try:
                entry = index[token]
            except KeyError:
                index[token] = []
                entry = index[token]
            finally:
                if pid not in entry:
                    entry.append(pid)
            self._do_index_words(names, pid)

    def _do_index_words(self, names: list, pid: str):
        index = self.indices['words']
        words = []
        for name in names:
            name_parts = name.split()
            if len(name_parts) > 1:
                words.extend(name_parts)
        words = [w.strip() for w in words if w is not None and w.strip() != '']
        tokens = [self._tokenize(w) for w in words]
        tokens = list(set(tokens))
        tokens = [t for t in tokens if t not in ['untitled', 'unnamed']]
        for token in tokens:
            try:
                entry = index[token]
            except KeyError:
                index[token] = []
                entry = index[token]
            finally:
                if pid not in entry:
                    entry.append(pid)

    def _do_index_modified(self, place):
        index = self.indices['modified']
        stamps = [place.data['created']]
        for event in place.data['history']:
            stamps.append(event['modified'])
        for location in place.data['locations']:
            stamps.append(location['created'])
            for event in location['history']:
                stamps.append(event['modified'])
        for name in place.data['names']:
            stamps.append(name['created'])
            for event in name['history']:
                stamps.append(event['modified'])
        stamps = list(set(stamps))
        stamps = sorted(stamps, reverse=True)
        try:
            latest = dateutil.parser.parse(stamps[0]).strftime('%Y%m%d')
        except TypeError:
            logger.critical(pformat(place.data))
            raise
        if latest > self.most_recent:
            self.most_recent = latest
        try:
            index[latest]
        except KeyError:
            index[latest] = []
        finally:
            pid = place.data['id']
            if pid not in index[latest]:
                index[latest].append(pid)

    def _get_index_last_modified(self):
        date_index = self.indices['modified']
        pid_index = self.indices['id']
        return [pid_index[pid] for pid in date_index[self.most_recent]]

    def _get_index_name(self, value):
        name_index = self.indices['name']
        pid_index = self.indices['id']
        token = self._tokenize(value)
        try:
            pids = name_index[token]
        except KeyError:
            return []
        return [pid_index[pid] for pid in pids]

    def _get_index_in_name(self, value):
        word_index = self.indices['words']
        logger.debug(
            'word index contains {} unique terms'.format(len(word_index)))
        pid_index = self.indices['id']
        token = self._tokenize(value)
        try:
            pids = word_index[token]
        except KeyError:
            logger.debug('word index MISS for token="{}"'.format(token))
            logger.debug(
                'index term context: {}'.format(
                    sorted(
                        [w for w in word_index.keys() if w.startswith(
                            token[0])])))
            return []
        else:
            logger.debug('word index HIT for token="{}": {} results'.format(
                token, len(pids)))
        return [pid_index[pid] for pid in pids]

    def _tokenize(self, raw: str):
        cooked = raw.strip()
        cooked = cooked.translate(punct_table)
        cooked = unidecode.unidecode(cooked)
        cooked = ''.join(cooked.split()).lower()
        return cooked

    def get(self, it, value=None):
        if it == 'id':
            try:
                result = self.indices['id'][value]
            except KeyError:
                return []
            else:
                return [result]
        else:
            if value is not None:
                return getattr(self, '_get_index_{}'.format(it))(value)
            else:
                return getattr(self, '_get_index_{}'.format(it))()

    def __add__(self, *args):
        if len(args) == 0:
            return self
        else:
            for pc in [a for a in args if isinstance(a, PlaceCollection)]:
                for p in pc.places:
                    self.add_place(p)
        return self
