# -*- coding: utf-8 -*-

# todo: inherit from set()
class MalFeedsCollection(object):
    def __init__(self):
        self._collection = {}

#class MalFeedsCollection(set):
#    def __init__(self, *args, **kwds):
#        super().__init__(*args, **kwds)

    def list(self):
        return self._collection.values()

    def add(self, malfeed):
        self._collection.update({malfeed.name: malfeed})

    def get(self, feedname):
        return self._collection[feedname]

    def delete(self, feedname):
        del self._collection[feedname]
