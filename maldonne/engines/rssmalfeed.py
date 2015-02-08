#!/usr/bin/env python

import hashlib
import feedparser
import time
import re


class MalRssFeed(object):
    def __init__(self, feedurl, feedtype):
        self._feed_url = feedurl
        self._feed_entry_type = feedtype
        self._feed_header = {}
        self._feed_entries = []

    def update(self):
        if self._feed_url is not None:
            self._feed_stream = feedparser.parse(self._feed_url)
            self._update_header()
            self._update_entries()

    def _update_header(self):
        rval = True
        _dfeeder = {
            'title': self._feed_stream.feed.get('title', None),
            'description': self._feed_stream.feed.get('description', None),
            'publisher': self._feed_stream.feed.get('publisher', None),
            'rights': self._feed_stream.feed.get('rights', None),
            'create_date': time.localtime(),
            'last_update': self._feed_stream.feed.get('updated_parsed',
                                                      time.localtime()),
            'last_status': self._feed_stream.get('status', '520')
        }
        self._feed_header.update(_dfeeder)
        return rval

    def _update_entries(self):
        rval = True
        for feeditem in self._feed_stream.entries:
            _item = {
                'id': '',
                'description': self._feed_stream.feed.get('title', ''),
                'domain': '',
                'create_date': time.localtime(),
                'last_update': self._feed_stream.feed.get('updated_parsed',
                                                          time.localtime()),
                'asn': '',
                'country': '',
                'coordinates': '',
                'ip': '',
                'url': ''
            }

            if self._feed_entry_type is not None:
                _item.update({self._feed_entry_type: feeditem.link})

            itemid_base = self._feed_stream.feed.get('link')
            _item['id'] = hashlib.md5(itemid_base.encode('utf-8')).hexdigest()
            self._feed_entries.append(_item)
        return rval
