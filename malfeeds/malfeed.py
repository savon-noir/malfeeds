#!/usr/bin/env python

import pprint
import hashlib
import feedparser
import time
import re


class MalwareDomainListFeed(object):
    def __init__(self):
        self._feed_url = 'http://www.malwaredomainlist.com/hostslist/mdl.xml'
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
            'publisher': self._feed_stream.feed.publisher if 'publisher' in self._feed_stream.feed else ''
        }
        return _dfeeder

    def _get_feed_entries(self):
        feed_entries = []

        for feeditem in self._feed_stream.entries:
            _item = {
                'id': feeditem.id,
                'domain': feeditem.link.split('=').pop(),
                'type': 'malware',
                'source': self._feed_stream.href,
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

            _ipmatch = re.search("IP address: ([^,]*),", feeditem.description).group(1)
            _parsed_ip = re.search("([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})", _ipmatch).group(1)

            _matched = re.search("Host: ([^,]*),", feeditem.description)
            _host_value = _matched.group(1)
            if _matched is not None:
                if _host_value == "-":
                    _item['ip'] = _parsed_ip
                    _item['url'] = _ipmatch
                else:
                    _item['url'] = _host_value
                    _item['ip'] = _parsed_ip
            else:
                continue

            print "----------------- START -----------------------------------"
            print feeditem.description
            pprint.pprint(_item)
            print "-----------------  END  ---------------------------------"
        return feed_entries


def main():
    mwfeed = MalwareDomainListFeed()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
