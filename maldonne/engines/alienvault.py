#!/usr/bin/env python

import hashlib
import requests
import time
import re


class AlienVaultFeed(object):
    def __init__(self):
        self._feed_base_url = 'http://reputation.alienvault.com/reputation.data'

        self._http_headers_time = "%a, %d %b %Y %H:%M:%S GMT"
        self._feed_header = {}
        self._feed_entries = []

        # will be later used for dumping unlisted entries
        r = requests.get(self._feed_base_url, stream=True, timeout=5)
        self._feed_header.update(self._get_feed_header(r))
        self._feed_entries.append(self._get_feed_entries(r, k))

    def _get_feed_header(self, resp):
        _dfeeder = {
            'id': hashlib.md5(self._feed_base_url).hexdigest(),
            'title': self._feed_base_url,
            'description': 'AlientVault Reputation list - alienvault.com',
            'last_status': resp.status_code,
            'url': self._feed_base_url,
            'publisher': 'alienvault.com'
        }

        if 'last-modified' in resp.headers:
            _updtime = time.strptime(resp.headers['last-modified'], self._http_headers_time)
            _dfeeder.update({'last_update': _updtime})
        else:
            _dfeeder.update({'last_update': time.localtime()})
        return _dfeeder

    def _get_feed_entries(self, resp, rtype):
        feed_entries = []
        if 'last-modified' in resp.headers:
            _updtime = time.strptime(resp.headers['last-modified'], self._http_headers_time)
        else:
            _updtime = time.localtime()

        _res = "IP"
        for feeditem in resp.iter_lines():
            if re.search("^\s*#.*", feeditem) is not None:
                continue

#In [124]: regexp = re.compile('((?:[0-9]{1,3}\.){3}[0-9]{1,3})#[0-9]#[0-9]#([^#]*)#((?:[^#]){0,2})#([^#]*)#([^#]*)')
#In [125]: b = regexp.search(a)
#In [126]: b.group(1)
#Out[126]: '112.125.32.145'
#In [127]: b.group(2)
#Out[127]: 'Scanning Host'
#In [128]: b.group(3)
#Out[128]: 'CN'
#In [129]: b.group(4)
#Out[129]: 'Beijing'
#In [130]: b.group(5)
#Out[130]: '39.9289016724,116.388298035'
#In [131]: b.group(6)

            _item = {
                'id': '',
                'domain': '',
                'resource': _res,
                'type': rtype,
                'tags': [_res, rtype],
                'source': self._feed_base_url,
                'last_update': _updtime,
                'asn': '',
                'country': '',
                'ip': feeditem.rstrip(),
                'url': ''
            }
            print "{0}: {1}".format(rtype, _item['ip'])
            itemid_base = "{0}/{1}".format(_item['source'], _item['ip'])
            _item['id'] = hashlib.md5(itemid_base).hexdigest()
            feed_entries.append(_item)
        return feed_entries


def main():
    mwfeed = OpenBLFeed()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
