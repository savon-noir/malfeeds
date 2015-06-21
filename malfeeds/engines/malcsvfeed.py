# -*- coding: utf-8 -*-

from malfeeds.engines import MalFeedEngine
import re


class MalCSVFeed(MalFeedEngine):
    def __init__(self, feedurl, feedtype, **kwargs):
        super(MalCSVFeed, self).__init__(feedurl, feedtype)
        self._commentchar = '#'
        self._delimiterchar = ';'
        self._csvpattern = '<{0}>'.format(feedtype)
        if 'comment' in kwargs:
            self._commentchar = kwargs['comment']
        if 'delimiter' in kwargs:
            self._delimiterchar = kwargs['delimiter']
        if 'pattern' in kwargs:
            self._csvpattern = kwargs['pattern']

        self._rule_pattern = ""
        for ikey in self._csvpattern.split(self._delimiterchar):
            self._rule_pattern += "(?P{0}[^{1}]*){1}".format(ikey, self._delimiterchar)
        self._rule_pattern.strip(self._delimiterchar)

    def _stream_iterator(self):
        return self._stream_iterator_http()

    def _iter_entry(self):
        for feeditem in self._feed_stream.iter_lines():
            if re.compile("^\s*{0}.*$".format(self._commentchar)).search(feeditem) is not None:
                continue

            _csvparsed = None
            m = re.compile("^\s*(.*)$").search(feeditem)
            if m is not None:
                itemvalue = m.group(1)
                if itemvalue is not None or len(itemvalue):
                    _csvparsed = re.search(self._rule_pattern, itemvalue)

            if _csvparsed is not None:
                _item = self._struct_entry
                _item.update(_csvparsed.groupdict())
                _item['last_update'] = self._feed_header['last_update']
                yield _item
