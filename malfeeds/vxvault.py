#!/usr/bin/env python

import hashlib
import requests
import time
import re


class VXVault(object):
    def __init__(self):
        self._feed_base_url = 'http://vxvault.siri-urz.net/URL_List.php'

        self._http_headers_time = "%a, %d %b %Y %H:%M:%S GMT"
        self._feed_header = {}
        self._feed_entries = []

        # will be later used for dumping unlisted entries
        r = requests.get(self._feed_base_url, stream=True, timeout=5)
        self._feed_header.update(self._get_feed_header(r))
        self._feed_entries.append(self._get_feed_entries(r, 'malware'))

    def _get_feed_header(self, resp):
        _dfeeder = {
            'id': hashlib.md5(self._feed_base_url).hexdigest(),
            'title': self._feed_base_url,
            'description': 'VXVault.net',
            'last_status': resp.status_code,
            'url': self._feed_base_url,
            'publisher': 'VXVault.net'
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

        _res = "URL"
        for feeditem in resp.iter_lines():
            if re.search("^\s*https?://", feeditem) is None:
                continue

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
                'url': feeditem.rstrip(),
                'ip': ''
            }
            print "{0}: {1}".format(rtype, _item['url'])
            itemid_base = "{0}/{1}".format(_item['source'], _item['url'])
            _item['id'] = hashlib.md5(itemid_base).hexdigest()
            feed_entries.append(_item)
        return feed_entries


def main():
    mwfeed = VXVault()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
