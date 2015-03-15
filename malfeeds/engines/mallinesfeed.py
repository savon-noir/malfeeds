#!/usr/bin/env python

import requests
import time
import re


class MalLinesFeed(object):
    def __init__(self, feedurl, feedtype, **kwargs):
        self._feed_url = feedurl
        self._feed_entry_type = feedtype
        self._feed_header = {}
        self._feed_entries = []
        self._http_headers_time = "%a, %d %b %Y %H:%M:%S GMT"
        self._commentchar = '#'
        if 'comment' in kwargs:
            self._commentchar = kwargs['comment']

    def update(self):
        if self._feed_url is not None:
            self._feed_stream = requests.get(self._feed_url, stream=True, timeout=120)
            self._update_header()
            self._update_entries()

    @property
    def feed_header(self):
        return self._feed_header

    @property
    def feed_entries(self):
        return self._feed_entries

    def _update_header(self):
        rval = True
        _dfeeder = {
            'create_date': time.localtime(),
            'last_update': None,
            'last_status': self._feed_stream.status_code
        }

        if 'last-modified' in self._feed_stream.headers:
            _updtime = time.strptime(self._feed_stream.headers['last-modified'], self._http_headers_time)
            _dfeeder.update({'last_update': _updtime})
        else:
            _dfeeder.update({'last_update': time.localtime()})

        self._feed_header.update(_dfeeder)
        return rval

    def _update_entries(self):
        rval = True
        known_garbage_list = ["Site", "[Adblock]", "<pre>"]
        if 'last-modified' in self._feed_stream.headers:
            _updtime = time.strptime(self._feed_stream.headers['last-modified'],
                                     self._http_headers_time)
        else:
            _updtime = time.localtime()

        for feeditem in self._feed_stream.iter_lines():
            if re.compile("^\s*{0}.*$".format(self._commentchar)).search(feeditem) is not None:
                continue
            _item = {
                'domain': '',
                'last_update': _updtime,
                'asn': '',
                'country': '',
                'coordinates': '',
                'ip': '',
                'url': ''
            }
            m = re.compile("^\s*([^;\s]*)\s*.*$").search(feeditem)
            if self._feed_entry_type is not None and m is not None:
                itemvalue = m.group(1)
                if itemvalue in known_garbage_list:
                    continue
                else:
                    _item.update({self._feed_entry_type: itemvalue})
            else:
                raise Exception("warning: no feed type specified. Ignoring entries")
            self._feed_entries.append(_item)
        return rval
