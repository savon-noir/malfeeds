#!/usr/bin/env python

import hashlib
import requests
import time
import re


class AlienVaultFeed(object):
    def __init__(self, config):
        self._feed_url = config.get('feedurl', None)
        self._feed_name = config.get('name', None)
        self._feed_header = {}
        self._feed_entries = []
        self._feed_config = config
        self._http_headers_time = "%a, %d %b %Y %H:%M:%S GMT"

    def update(self):
        if self._feed_url is not None:
            # will be later used for dumping unlisted entries
            self._feed_stream = requests.get(self._feed_url, stream=True, timeout=120)
            self._feed_header.update(self._get_feed_header(self._feed_stream))
            self._feed_entries.append(self._get_feed_entries(self._feed_stream))

    def _get_feed_header(self, resp):
        _pkeys = {'title': 'AlienVault List',
                  'description': 'AlientVault Reputation list - alienvault.com',
                  'publisher': 'AlienVault.com',
                  'rights': 'AlienVault'
        }

        for k in _pkeys.keys():
            if k in self._feed_config:
                _pkeys[k] = self._feed_config.get(k, None)

        _dfeeder = {
            'id': hashlib.md5(self._feed_url).hexdigest(),
            'title': _pkeys['title'],
            'description': _pkeys['description'],
            'create_date': time.localtime(),
            'last_update': None,
            'last_status': resp.status_code,
            'feedurl': self._feed_url,
            'publisher': _pkeys['publisher'],
            'rights': _pkeys['rights']
        }

        if 'last-modified' in resp.headers:
            _updtime = time.strptime(resp.headers['last-modified'], self._http_headers_time)
            _dfeeder.update({'last_update': _updtime})
        else:
            _dfeeder.update({'last_update': time.localtime()})
        return _dfeeder

    def _get_feed_entries(self, resp):
        feed_entries = []
        if 'last-modified' in resp.headers:
            _updtime = time.strptime(resp.headers['last-modified'], self._http_headers_time)
        else:
            _updtime = time.localtime()

        for feeditem in resp.iter_lines():
            if re.search("^\s*#.*", feeditem) is not None:
                continue
            regexp = re.compile('((?:[0-9]{1,3}\.){3}[0-9]{1,3})#[0-9]#[0-9]#([^#]*)#((?:[^#]){0,2})#([^#]*)#([^#]*)')
            regres = regexp.search(feeditem)
            print feeditem
            if regres is not None:
                _ip = regres.group(1)
                _country = regres.group(3)
                _coordinates = regres.group(5)

            _item = {
                'id': '',
                'domain': _ip,
                'type': self._feed_config.get('type', None),
                'tags': self._feed_config.get('tags', []),
                'feedname': self._feed_name,
                'last_update': _updtime,
                'asn': '',
                'country': _country,
                'coordinates': _coordinates,
                'ip': _ip,
                'url': 'http://{0}/'.format(_ip)
            }
            itemid_base = "{0}/{1}".format(_item['feedname'], _item['ip'])
            _item['id'] = hashlib.md5(itemid_base).hexdigest()
            print _item
            feed_entries.append(_item)
        return feed_entries
