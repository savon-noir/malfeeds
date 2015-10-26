# -*- coding: utf-8 -*-

from malfeeds.engines import MalFeedEngine
from malfeeds.library import get_item_type
import re


class MalTcpdFeed(MalFeedEngine):
    def __init__(self, feedurl, feedtype, input_type, **kwargs):
        super(MalTcpdFeed, self).__init__(feedurl, feedtype, input_type)
        self._commentchar = '#'
        if 'comment' in kwargs:
            self._commentchar = kwargs['comment']

    def _iter_entry(self):
        for feeditem in self._feed_stream.iter_lines():
            _itemvalue = ''
            if re.compile("^\s*{0}.*$".format(self._commentchar)).search(feeditem) is not None:
                continue
            regres = re.compile('^.*:\s*(\S*).*$').search(feeditem)
            if regres is not None:
                _itemvalue = regres.group(1)
            
            _item = self._struct_entry
            _itype = get_item_type(_itemvalue)
            if _itype is None:
                _itype = self._feed_entry_type
            _item[_itype] = _itemvalue
            _item['type'] = _itype
            _item['last_update'] = self._feed_header['last_update']
            yield _item
