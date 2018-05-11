# pleiades.walker

This package is designed to facilitate work with [Pleiades](https://pleiades.stoa.org) JSON files distributed in [a hierarchical directory structure like that created by pleiades-datasets](https://github.com/isawnyu/pleiades-datasets#javascript-object-notation-json).

One might use it to read in all the data like this:

```python
>>> from pleiades.walker.walker import PleiadesWalker
>>> walker = PleiadesWalker(path='../pleiades-datasets/json')
>>> place_count, place_collection = walker.walk()
>>> print(place_count)
35777
```

The ```PlaceCollection``` class is defined in the ```pleiades.walker.entities``` module. It provides a public ```get()``` method that lets one interrogate some aspects of the data, returning a list of ```pleiades.walker.entities.Place``` objects:

```python
>>> places = place_collection.get(it='id', value='963101351')
>>> type(places)
<class 'list'>
>>> len(places)
1
>>> p = places[0]
>>> type(p)
<class 'pleiades.walker.entities.Place'>
```

The ```PlaceCollection``` class currently supports queries against the following indexes, constructing them in memory the first time they are called in the life of the instance:

 - 'id': returns the place with the corresponding Pleiades ID
 - 'name': returns a list of places with names matching the requested value
 - 'last_modified': returns the most recently modified places (the "value" parameter is ignored)
 - 'in_name': returns a list of places whose names contain the word or phrase in the value parameter

An instance of the  ```Place``` class stores all the information from the source JSON file in its "data" attribute:

```python
>>> from pprint import pprint
>>> pprint(p.data, indent=4)
{   '@type': 'Place',
    'bbox': [10.516354, 33.631538, 10.516354, 33.631538],
    'connectsWith': [],
    'contributors': [   {   'homepage': None,
                            'name': 'Sean Gillies',
                            'uri': 'https://pleiades.stoa.org/author/sgillies',
                            'username': 'sgillies'},
                        {   'homepage': None,
                            'name': 'Tom Elliott',
                            'uri': 'https://pleiades.stoa.org/author/thomase',
                            'username': 'thomase'}],
    'created': '2011-09-09T21:30:35Z',
    'creators': [{'name': 'DARMC', 'username': None}],
    'description': 'An unnamed villa of Tripolitana',
    'details': '',
    'features': [   {   'geometry': {   'coordinates': [10.516354, 33.631538],
                                        'type': 'Point'},
                        'id': 'darmc-location-26860',
                        'properties': {   'description': '500K scale point '
                                                         'location',
                                          'link': 'https://pleiades.stoa.org/places/963101351/darmc-location-26860',
                                          'location_precision': 'precise',
                                          'snippet': 'Unknown',
                                          'title': 'DARMC location 26860'},
                        'type': 'Feature'}],
    'history': [   {   'comment': 'Location updates and tags from Johan '
                                  "Ahlfeldt's (jahlfeldt) Digital Atlas of the "
                                  'Roman Empire in October 2012',
                       'modified': '2012-10-21T00:24:04Z',
                       'modifiedBy': 'sgillies'},
                   {   'comment': 'Global migration and reindexing of '
                                  'citations and provenance, February 2012',
                       'modified': '2012-02-15T09:52:28Z',
                       'modifiedBy': 'admin'},
                   {   'comment': 'New locations, coordinates, and metadata '
                                  "from Harvard's DARMC project. See "
                                  'http://atlantides.org/trac/pleiades/wiki/PlaceUpgradesAndMigrations. '
                                  'Cloned from master place: 324841375.',
                       'modified': '2011-09-09T21:30:37Z',
                       'modifiedBy': 'sgillies'}],
    'id': '963101351',
    'locations': [   {   '@type': 'Location',
                         'accuracy': 'https://pleiades.stoa.org/features/metadata/darmc-c',
                         'archaeologicalRemains': 'unknown',
                         'associationCertainty': 'certain',
                         'attestations': [],
                         'contributors': [{'name': 'DARMC', 'username': None}],
                         'created': '2011-09-09T21:30:36Z',
                         'creators': [   {   'homepage': None,
                                             'name': 'Sean Gillies',
                                             'uri': 'https://pleiades.stoa.org/author/sgillies',
                                             'username': 'sgillies'}],
                         'description': '500K scale point location',
                         'details': 'DARMC OBJECTID: 26860',
                         'end': None,
                         'featureType': ['unknown'],
                         'geometry': {   'coordinates': [10.516354, 33.631538],
                                         'type': 'Point'},
                         'history': [   {   'comment': 'Global migration and '
                                                       'reindexing of '
                                                       'citations and '
                                                       'provenance, February '
                                                       '2012',
                                            'modified': '2012-02-15T09:52:29Z',
                                            'modifiedBy': 'admin'},
                                        {   'comment': 'New locations, '
                                                       'coordinates, and '
                                                       'metadata from '
                                                       "Harvard's DARMC "
                                                       'project. See '
                                                       'http://atlantides.org/trac/pleiades/wiki/PlaceUpgradesAndMigrations.',
                                            'modified': '2011-09-09T21:30:36Z',
                                            'modifiedBy': 'sgillies'}],
                         'id': 'darmc-location-26860',
                         'locationType': ['representative'],
                         'provenance': 'DARMC OBJECTID: 26860',
                         'references': [   {   'accessURI': 'http://darmc.harvard.edu',
                                               'alternateURI': '',
                                               'bibliographicURI': '',
                                               'citationDetail': '',
                                               'formattedCitation': 'Michael '
                                                                    'McCormick, '
                                                                    'Guoping '
                                                                    'Huang, '
                                                                    'Kelly '
                                                                    'Gibson et '
                                                                    'al. '
                                                                    '(ed.), '
                                                                    'Digital '
                                                                    'Atlas of '
                                                                    'Roman and '
                                                                    'Medieval '
                                                                    'Civilizations, '
                                                                    'Harvard '
                                                                    'University '
                                                                    'Center '
                                                                    'for '
                                                                    'Geographic '
                                                                    'Analysis',
                                               'otherIdentifier': ' ',
                                               'shortTitle': '',
                                               'type': 'cites'}],
                         'review_state': 'published',
                         'start': None,
                         'title': 'DARMC location 26860',
                         'uri': 'https://pleiades.stoa.org/places/963101351/darmc-location-26860'}],
    'names': [],
    'placeTypes': ['villa'],
    'provenance': 'Barrington Atlas: BAtlas 35',
    'references': [   {   'accessURI': '',
                          'alternateURI': '',
                          'bibliographicURI': 'http://openlibrary.org/works/OL8327792W',
                          'citationDetail': '',
                          'formattedCitation': 'BAtlas 35',
                          'otherIdentifier': ' ',
                          'shortTitle': '',
                          'type': 'seeFurther'}],
    'reprPoint': [10.516354, 33.631538],
    'review_state': 'published',
    'rights': 'Copyright © The Contributors. Sharing and remixing permitted '
              'under terms of the Creative Commons Attribution 3.0 License '
              '(cc-by).',
    'subject': ['dare:major=0', 'dare:ancient=2', 'dare:feature=villa'],
    'title': 'Unnamed villa',
    'type': 'FeatureCollection',
    'uri': 'https://pleiades.stoa.org/places/963101351'}
```

The tests may be helpful. 
