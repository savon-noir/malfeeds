#!/usr/bin/env python

import hashlib
import feedparser
import time
import re


class MalRssFeed(object):
    def __init__(self, feedname, config):
        self._feed_url = config.get('feedurl', None)
        self._feed_header = {}
        self._feed_entries = []
        self._feed_name = feedname
        self._config = config

        if self._feed_url is not None:
            self._feed_stream = feedparser.parse(self._feed_url)
            self._feed_header.update(self._get_feed_header())
            self._feed_entries = self._get_feed_entries()

    def _get_feed_header(self):
        _pkeys = {'title': '',
                  'description': '',
                  'publisher': '',
                  'rights': ''
                  }

        for k in _pkeys.keys():
            if k in self._config:
                _pkeys[k] = self._config.get(k, None)
            else:
                _pkeys[k] = self._feed_stream.feed.get(k, '')

        _dfeeder = {
            'id': hashlib.md5(self._feed_stream.href).hexdigest(),
            'title': _pkeys['title'],
            'description': _pkeys['description'],
            'rights': _pkeys['rights'],
            'create_date': time.localtime(),
            'last_update': self._feed_stream.feed.get('updated_parsed',
                                                      time.localtime()),
            'status': self._feed_stream.get('status', '520'),
            'feedurl': self._feed_stream.href,
            'publisher': self._feed_name
        }
        return _dfeeder

    def _get_feed_entries(self):
        feed_entries = []

        for feeditem in self._feed_stream.entries:
            _item = {
                'id': '',
                # TODO: derivate domain from URL
                'domain': feeditem.link.split('=').pop(),
                'type': self._config.get('type', None),
                'publisher': self._feed_name,
                'last_update': self._feed_stream.feed.get('updated_parsed',
                                                          self. time.localtime()),
                'asn': '',
                'country': '',
                'ip': '',
                'url': ''
            }

            if self._config.getint('use_geoip') == 0:
                _matched = re.search("ASN: ([^,]*),", feeditem.description)
                if _matched is not None:
                    _item['asn'] = _matched.group(1)

                _matched = re.search("Country: ([^,]*),", feeditem.description)
                if _matched is not None:
                    _item['country'] = _matched.group(1)
            else:
                print "USE GEOIP"

            if self._config.getint('use_dns') == 0:
                _ipmatch = re.search("IP [aA]ddress: ([^,]*),", feeditem.description).group(1)
                _parsed_ip = re.search("([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})", _ipmatch).group(1)

            _matched = re.search("(?:Host|URL): ([^,]*),", feeditem.description)
            if _matched is not None:
                _host_value = _matched.group(1)
                if _host_value == "-":
                    _item['ip'] = _parsed_ip
                    _item['url'] = _ipmatch
                else:
                    _item['url'] = _host_value
                    _item['ip'] = _parsed_ip
            else:
                raise Exception("NO HOST OR URL ENTRY")

            itemid_base = _item['publisher'] + _item['url']
            _item['id'] = hashlib.md5(itemid_base.encode('utf-8')).hexdigest()
            feed_entries.append(_item)
        return feed_entries
