# -*- coding: utf-8 -*-

import re


class FeedIOC(object):
    def __init__(self, malitemdict):
        self._itemdict = malitemdict

        self.id = None
        self.last_update = None
        self.create_date = None
        self.description = ''
        self.type = None
        self.url = None
        self.ip = None
        self.domain = None
        self.asn = None
        self.country = None
        self.coordinates = None
        self.tags = None

    def extended_attributes(self, iocdata):
        extattr_dict = {}
        mdict = {
            'asn': "ASN: ([^,]*),",
            'country': "Country: ([^,]*),",
            'ip': "IP [aA]ddress: ([^,]*),",
            'url': "(?:Host|URL): ([^,]*),"
        }

        for mkey in mdict.keys():
            _matched = re.search(mdict[mkey], iocdata)
            if _matched is not None:
                extattr_dict.update({mkey: _matched.group(1)})

        if 'url' not in extattr_dict and 'ip' in extattr_dict:
            extattr_dict['url'] = "http://{0}/".format(extattr_dict['ip'])

        if 'url' in extattr_dict and 'ip' in extattr_dict and extattr_dict['url'] == "-":
            extattr_dict['url'] = "http://{0}/".format(extattr_dict['ip'])

        return extattr_dict
