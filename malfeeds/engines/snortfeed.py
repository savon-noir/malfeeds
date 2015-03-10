#!/usr/bin/env python

import requests
import time
import re
from idstools.rule import parse_fileobj


def extract_itemslist(rawdata):
    ruleitems = []
    actions = ("alert", "log", "pass", "activate", "dynamic", "drop", "reject", "sdrop")
    rule_pattern = re.compile(
        r"^(?P<enabled>#)*\s*"
        r"(?P<raw>"
        r"(?P<action>%s)\s*"
        r"(?:udp|tcp)\s*"
        r"(?:\[)*(?P<source>[^\s\]]*)(?:\])*\s*"
        r"[^\s]*\s*"
        r"(?P<direction>[-><]+)\s*"
        r"(?:\[)*(?P<destination>[^\s\]]*)(?:\])*\s*"
        r"[^\s]*\s*"
        r")"
        % "|".join(actions))

    m = rule_pattern.match(rawdata)
    if m is not None:
        srcitems = m.group("source")
        dstitems = m.group("destination")
        ruleitems += [h.strip(' ') for h in srcitems.split(',')]
        ruleitems += [h.strip(' ') for h in dstitems.split(',')]

        junk = ['$HOME_NET', '', 'any']
        ruleitems = filter(lambda x: x not in junk, ruleitems)
    return ruleitems

def check_ip(item):
    ip = None
    regres = re.compile('\s*([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})\s*').search(item)
    if regres is not None:
        ip = regres.group(1)
    return ip


def check_subnet(item):
    subnet = None
    regres = re.compile('\s*([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\/[0-9]{1,2})*\s').search(item)
    if regres is not None:
        subnet = regres.group(1)
    return subnet

def get_item_type(item, default='ip'):
    itype = default
    if check_ip(item) is not None:
        itype = 'ip'
    elif check_subnet(item) is not None:
        itype = 'domain'
    return itype


class MalSnortFeed(object):
    def __init__(self, feedurl, feedtype):
        self._feed_url = feedurl
        self._feed_entry_type = feedtype
        self._feed_header = {}
        self._feed_entries = []
        self._http_headers_time = "%a, %d %b %Y %H:%M:%S GMT"

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
        if 'last-modified' in self._feed_stream.headers:
            _updtime = time.strptime(self._feed_stream.headers['last-modified'],
                                     self._http_headers_time)
        else:
            _updtime = time.localtime()

        ruleslist = parse_fileobj(self._feed_stream.raw)
        for rule in ruleslist:
            rawdata = rule['raw']
            itemslist = extract_itemslist(rawdata)

            for feeditem in itemslist:
                _item = {
                    'last_update': _updtime,
                    'description': rule['msg'],
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
                itype = get_item_type(feeditem)
                _item.update({'type': itype, itype: feeditem})

                self._feed_entries.append(_item)
        return rval
