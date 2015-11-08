# -*- coding: utf-8 -*-

from malfeeds.engines import MalFeedEngine
import logging
import time
import re


class TORExitNodesFeed(MalFeedEngine):
    def __init__(self, feedurl, feedtype, input_type, **kwargs):
        super(TORExitNodesFeed, self).__init__(feedurl, feedtype, input_type, **kwargs)
        self._commentchar = '#'
        if 'comment' in kwargs:
            self._commentchar = kwargs['comment']

    def _iter_entry(self):
        torlist = []
        btemplate = {
            'nodename': '',
            'create_date': '',
            'last_update': '',
            'ip': ''
        }

        for feeditem in self._feed_stream.iter_lines():
            if re.compile("^\s*{0}.*$".format(self._commentchar)).search(feeditem) is not None:
                continue
            if feeditem.startswith('ExitNode'):
                _item = self._struct_entry
                _item['name'] = feeditem.split()[1]
            elif feeditem.startswith('Published'):
                _item['create_date'] = time.strptime(' '.join(feeditem.split()[1:]), '%Y-%m-%d %H:%M:%S')
            elif feeditem.startswith('LastStatus'):
                _item['last_update'] = time.strptime(' '.join(feeditem.split()[1:]), '%Y-%m-%d %H:%M:%S')
            elif feeditem.startswith('ExitAddress'):
                _item['type'] = 'ip'
                _item['ip'] = feeditem.split()[1]
                yield _item
            else:
                raise Exception("warning: no feed type specified. Ignoring entries")
                logging.error("unknown line read from input stream with content {0}".format(feeditem))
