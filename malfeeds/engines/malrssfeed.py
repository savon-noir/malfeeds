# -*- coding: utf-8 -*-

from malfeeds.engines import MalFeedEngine


class MalRSSFeed(MalFeedEngine):
    def __init__(self, feedurl, feedtype, **kwargs):
        super(MalRSSFeed, self).__init__(feedurl, feedtype)

    def _stream_iterator(self):
        return self._stream_iterator_rss()

    def _update_entries(self):
        rval = True
        for feeditem in self._feed_stream.entries:
            _item = self._struct_entry.copy()
            _item[self._feed_entry_type] = feeditem.link
            _item['last_update'] = self._feed_header['last_update']
            _item['description'] = feeditem.get('description', '')
            self._feed_entries.append(_item)
        return rval
