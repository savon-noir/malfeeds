#!/usr/bin/env python

import requests
import time
import re


class AlienVaultFeed(object):
    def __init__(self, feedurl, feedtype):
        self._feed_url = feedurl
        self._feed_entry_type = feedtype
        self._feed_header = {}
        self._feed_entries = []
        self._http_headers_time = "%a, %d %b %Y %H:%M:%S GMT"

    def update(self):
        if self._feed_url is not None:
            # will be later used for dumping unlisted entries
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
        if 'last-modified' in self._feed_stream.headers:
            _updtime = time.strptime(self._feed_stream.headers['last-modified'],
                                     self._http_headers_time)
        else:
            _updtime = time.localtime()

        for feeditem in self._feed_stream.iter_lines():
            if re.search("^\s*#.*", feeditem) is not None:
                continue
            regexp = re.compile('((?:[0-9]{1,3}\.){3}[0-9]{1,3})#[0-9]#[0-9]#([^#]*)#((?:[^#]){0,2})#([^#]*)#([^#]*)')
            regres = regexp.search(feeditem)
            if regres is not None:
                _ip = regres.group(1)
                _country = regres.group(3)
                _coordinates = regres.group(5)

            _item = {
                'description': '',
                'domain': '',
                'last_update': _updtime,
                'asn': '',
                'country': _country,
                'coordinates': _coordinates,
                'ip': _ip,
                'url': ''
            }
            self._feed_entries.append(_item)
        return rval
