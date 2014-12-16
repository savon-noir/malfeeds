#!/usr/bin/env python

import hashlib
import feedparser
import time
import re


class MalFeed(object):
    def __init__(self, url):
        self._feed_url = url
        self._feed_header = {}
        self._feed_entries = []
        self._feed_stream = feedparser.parse(self._feed_url)
        self._feed_header.update(self._get_feed_header())
        self._feed_entries = self._get_feed_entries()

    def _get_feed_header(self):
        _dfeeder = {
            'id': hashlib.md5(self._feed_stream.href).hexdigest(),
            'title': self._feed_stream.feed.title if 'title' in self._feed_stream.feed else '',
            'description': self._feed_stream.feed.subtitle if 'subtitle' in self._feed_stream.feed else '',
            'last_update': self._feed_stream.feed.updated_parsed if 'updated_parsed' in self._feed_stream.feed else time.localtime(),
            'last_status': self._feed_stream.status if 'status' in self._feed_stream else '520',
            'url': self._feed_stream.href,
            'publisher': self._feed_stream.feed.rights if 'rights' in self._feed_stream.feed else ''
        }
        return _dfeeder

    def _get_feed_entries(self):
        feed_entries = []

        for feeditem in self._feed_stream.entries:
            _item = {
                'id': '',
                'domain': feeditem.link.split('=').pop(),
                'type': 'malware',
                'source': None,
                'last_update':  self._feed_stream.feed.updated_parsed if 'updated_parsed' in self._feed_stream.feed else time.localtime(),
                'asn': '',
                'country': '',
                'ip': '',
                'url': ''
            }
            _matched = re.search("ASN: ([^,]*),", feeditem.description)
            if _matched is not None:
                _item['asn'] = _matched.group(1)
            _matched = re.search("Country: ([^,]*),", feeditem.description)
            if _matched is not None:
                _item['country'] = _matched.group(1)
            feed_entries.append(_item)

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

            if 'summary_detail' in feeditem:
                _item['source'] = feeditem.summary_detail.base if 'base' in feeditem.summary_detail else None

            itemid_base = "{0}/{1}".format(_item['source'], _item['url'])
            _item['id'] = hashlib.md5(itemid_base).hexdigest()
            # dl4.getz.tv
            print "------------------"
            print feeditem
            print "(", _item['url'], ")"
        return feed_entries


def main():
    mwfeed = MalFeed('http://malc0de.com/rss/')
    mwfeed = MalFeed('http://www.malwaredomainlist.com/hostslist/mdl.xml')

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
