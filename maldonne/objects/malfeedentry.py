# -*- coding: utf-8 -*-

import re
import hashlib


class MalFeedEntry(object):
    def __init__(self, malitemdict, extended=0):
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
        self.sha1 = None
        self.md5 = None

        self.__dict__.update(malitemdict)
        if extended:
            self.__dict__.update(self.extended_attributes(self.description))

        itemid_base = "{0}={1}".format(self.feedurl.encode('utf-8'), getattr(self, self.type).encode('utf-8'))
        self.id = hashlib.md5(itemid_base).hexdigest()


    def extended_attributes(self, iocdata):
        extattr_dict = {}
        mdict = {
            'asn': "ASN: (\w*)",
            'country': "Country: (\w*)",
            'ip': "IP [aA]ddress: (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})",
            'url': "(?:Host|URL): ([^\s,]*)",
            'md5': "MD5.*: (\w*)"
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
