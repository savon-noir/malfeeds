#!/usr/bin/env python

import hashlib
import requests
import time
import re


class OpenBLFeed(object):
    def __init__(self):
        self._feed_base_url = 'https://www.openbl.org/lists/'

        openbltypes = {
            "SSH": "base_all_ssh-only.txt",
            "HTTP": "base_all_http-only.txt",
            "FTP": "base_all_ftp-only.txt",
            "MAIL": "base_all_mail-only.txt",
            "SMTP": "base_all_smtp-only.txt"
        }
        self._http_headers_time = "%a, %d %b %Y %H:%M:%S GMT"
        self._feed_header = {}
        self._feed_entries = []

        # will be later used for dumping unlisted entries
        r = requests.get("{0}{1}".format(self._feed_base_url, "delisted.txt"), stream=True, timeout=5)
        self._feed_header.update(self._get_feed_header(r))

        for k in openbltypes.keys():
            r = requests.get("{0}{1}".format(self._feed_base_url, openbltypes[k]), stream=True, timeout=5)
            self._feed_entries.append(self._get_feed_entries(r, k))

    def _get_feed_header(self, resp):
        _dfeeder = {
            'id': hashlib.md5(self._feed_base_url).hexdigest(),
            'title': self._feed_base_url,
            'description': 'OpenBL Blacklist - OpenBL.org',
            'last_status': resp.headers.get('status_code', '520'),
            'url': self._feed_base_url,
            'publisher': 'openbl.org'
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
