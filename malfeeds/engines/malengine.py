# -*- coding: utf-8 -*-

import requests
from requests.exceptions import ConnectionError
from pwd import getpwuid
import feedparser
import time
import socket
import os


class MalFeedEngine(object):
    def __init__(self, feeduri, feedtype, input_type):
        self._feed_url = feeduri
        self._feed_entry_type = feedtype
        self._feed_header = {}
        self._feed_stream = None

        self.timeout = 4
        self.iterator_type = None

        self._input_type = input_type

        self._feed_header = {
            'title': None,
            'description': '',
            'publisher': '',
            'rights': '',
            'create_date': time.localtime(),
            'last_update': '',
            'last_status': 'READY',  # READY, OK, FAILED
        }

    @property
    def _struct_entry(self):
        return {
            'create_date': time.localtime(),
            'last_update': '',
            'description': '',
            'type': '',
            'url': '',
            'domain': '',
            'ip': '',
            'subnet': '',
            'email': '',
            'asn': '',
            'country': '',
            'coordinates': '',
            'md5': '',
            'sha1': ''
        }

    def update(self):
        if self._feed_url is not None:
            self._feed_stream = self._stream_iterator()
            self._update_header()

    @property
    def feed_header(self):
        return self._feed_header

    @property
    def feed_entries(self):
        return self._iter_entry()

    def _stream_iterator(self):
        sptr = {'http': self._stream_iterator_http,
                'rss': self._stream_iterator_rss,
                'file': self._stream_iterator_file
        }
        return sptr[self._input_type]

    def _stream_iterator_http(self):
        self.iterator_type = 'http'
        rit = None
        try:
            rit = requests.get(self._feed_url, stream=True, timeout=self.timeout)
        except ConnectionError:
            raise Exception("Failed to connect to url: {0}".format(self._feed_url)) 
        return rit

    def _stream_iterator_rss(self):
        socket.setdefaulttimeout(self.timeout)
        self.iterator_type = 'rss'
        rit = feedparser.parse(self._feed_url)
        if 'bozo_exception' in rit:
            raise Exception("Failed to connect to rss feed: {0}".format(self._feed_url))
        return rit

    def _stream_iterator_file(self):
        self.iterator_type = 'file'
        rit = None
        try:
            rit = open(self._feed_url, 'r', encoding='utf-8')
        except IOError:
            raise Exception("Failed to open file {0}".format(self._feed_url))
        return rit

    def _update_header(self):
        if self.iterator_type == "http":
            self._update_header_http()
        elif self.iterator_type == "rss":
            self._update_header_rss()
        elif self.iterator_type == "file":
            self._update_header_file()
        else:
            raise Exception("Unknown stream type configured. Implement specific _update_header method in engine")

    def _update_header_http(self):
        http_headers_time = "%a, %d %b %Y %H:%M:%S GMT"
        rval = True
        lstatus = "READY"
        lmodified = time.localtime()
        if self._feed_stream is not None:
            sc = self._feed_stream.status_code
            if sc >= 200 and sc < 400:
                lstatus = "OK"
            elif sc >= 500:
                lstatus = "FAILED"
            else:
                rval = False

            if 'last-modified' in self._feed_stream.headers:
                lmodified = time.strptime(self._feed_stream.headers['last-modified'], http_headers_time)
            else:
                rval = False
        else:
            rval = False

        _dfeeder = {
            'create_date': time.localtime(),
            'last_update': lmodified,
            'last_status': lstatus
        }

        self._feed_header.update(_dfeeder)
        return rval

    def _update_header_rss(self):
        rval = True

        lstatus = "READY"
        sc = int(self._feed_stream.get('status', 520))
        if sc >= 200 and sc < 400:
            lstatus = "OK"
        elif sc >= 500:
            lstatus = "FAILED"

        _dfeeder = {
            'title': self._feed_stream.feed.get('title', None),
            'description': self._feed_stream.feed.get('description', ''),
            'publisher': self._feed_stream.feed.get('publisher', ''),
            'rights': self._feed_stream.feed.get('rights', ''),
            'create_date': time.localtime(),
            'last_update': self._feed_stream.feed.get('updated_parsed',
                                                      time.localtime()),
            'last_status': lstatus
        }
        if _dfeeder['title'] is None:
            rval = False

        self._feed_header.update(_dfeeder)
        return rval

    def _update_header_file(self):
        rval = True
        lstatus = "READY"
        try:
            fstat = os.stat(self._feed_url)
        except OSError:
            lstatus = "FAILED"

        if self._feed_stream is None:
            lstatus = "FAILED"

        _owner = getpwuid(fstat.st_uid).pw_name
        _dfeeder = {
            'title': os.path.basename(self._feed_url),
            'description': self._feed_url,
            'publisher': _owner,
            'rights': _owner,
            'create_date': time.localtime(fstat.st_ctime),
            'last_update': time.localtime(fstat.st_mtime),
            'last_status': lstatus
        }
        if _dfeeder['title'] is None:
            rval = False

        self._feed_header.update(_dfeeder)

        return rval
