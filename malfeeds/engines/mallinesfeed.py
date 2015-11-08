# -*- coding: utf-8 -*-

from malfeeds.engines import MalFeedEngine
from malfeeds.library import get_clean_item, get_item_type
import re


class MalLinesFeed(MalFeedEngine):
    def __init__(self, feedurl, feedtype, input_type, **kwargs):
        super(MalLinesFeed, self).__init__(feedurl, feedtype, input_type, **kwargs)
        self._commentchar = '#'
        if 'comment' in kwargs:
            self._commentchar = kwargs['comment']

    def _iter_entry(self):
        known_garbage_list = ["Site", "[Adblock]", "<pre>"]

        for feeditem in self._feed_stream.iter_lines():
            if re.compile("^\s*{0}.*$".format(self._commentchar)).search(feeditem) is not None:
                continue
            m = re.compile("^\s*([^;\s]*)\s*.*$").search(feeditem)
            if self._feed_entry_type is not None and m is not None:
                _itype = get_item_type(m.group(1))
                if _itype is None:
                    _itype = self._feed_entry_type
                itemvalue = get_clean_item(m.group(1), _itype)
                if itemvalue is None or itemvalue in known_garbage_list or not len(itemvalue):
                    continue
                else:
                    _item = self._struct_entry
                    _item[_itype] = itemvalue
                    _item['last_update'] = self._feed_header['last_update']
                    _item['type'] = _itype
                    yield _item
            else:
                raise Exception("warning: no feed type specified. Ignoring entries")
