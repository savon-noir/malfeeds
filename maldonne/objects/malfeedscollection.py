# -*- coding: utf-8 -*-

class MalFeedsCollection(set):
    def __init__(self, *args, **kwds):
        super(MalFeedsCollection, self).__init__(*args, **kwds)
        self._collection = []

    def get(self, feedname):
        pass
