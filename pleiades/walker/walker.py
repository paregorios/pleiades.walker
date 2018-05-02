#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Walk a directory tree and perform customizeable actions."""

import logging
import json
from os import walk
from os.path import abspath, isdir, join, realpath, splitext
from pleiades.walker import PlaceCollection

logger = logging.getLogger(__name__)


class Walker():
    """Selectively visit files in a tree and act on them.

    The following public methods are available:

    - __init__(): takes two arguments when constructing an instance:
      - path: the path to the root of the subtree that is to be walked
      - extensions: a list of strings, each containing a filename extension
        (including the leading '.') to be considered when acting on files found
        in a directory. An empty extensions argument (the default) means that
        all regular files found will be addressed.

    - walk(): Walk the directory subtree rooted at the path specified when
      the instance was constructed. For each batch of files considered (see the
      'extensions' argument to __init__()), the internal '_do()' method is
      called.

    The _do() method:

    Override this method in a subclass in order to specify fun things to do
    to the files that walk() finds.
    """

    def __init__(self, path: str, extensions=[]):
        self.path = abspath(realpath(path))
        if not isdir(self.path):
            raise IOError(
                '{} is not a valid directory path'.format(self.path))
        self.count = False
        self.extensions = [e.lower() for e in extensions]

    def walk(self, count=True):
        if count:
            self.count = 0
        results = None
        for root, dirs, files in walk(self.path):
            logger.debug('at {}: {}'.format(root, repr(files)))
            if len(self.extensions) > 0:
                select_files = [
                    f for f in files if splitext(f)[1].lower()
                    in self.extensions]
            else:
                select_files = files
            logger.debug('selected files: {}'.format(sorted(select_files)))
            if count:
                self.count += len(select_files)
            data = self._load(root, select_files)
            data = self._clean(data)
            result = self._do(data)
            if results is None:
                results = result
            else:
                results += result
        return (self.count, results)

    def _load(self, root, filenames):
        """Perform some action on files at a directory node."""

        data = []
        for filename in filenames:
            with open(join(root, filename), 'r') as f:
                data.append(f.read())
            del f
        return data

    def _clean(self, data: list):
        """Cleanup the data you loaded."""
        return data

    def _do(self, data: list):
        """Do something with the data you loaded in self._load."""
        pass


class JsonWalker(Walker):
    """A class to crawl a hierarchical directory tree JSON files.
    """

    def __init__(self, path):
        """Initialize the class."""
        super().__init__(path=path, extensions=['.json'])

    def _load(self, root, filenames):

        data = []
        for filename in filenames:
            with open(join(root, filename), 'r', encoding='utf-8') as f:
                data.append(json.load(f))
            del f
        return data


class PleiadesWalker(JsonWalker):
    """A class to crawl a hierarchical directory of Pleiades JSON files.
    """

    def __init__(self, path):
        super().__init__(path=path)

    def _do(self, data: list):
        pc = PlaceCollection()
        for datum in data:
            pc.add_place(datum)
        return pc
