# -*- coding: utf-8 -*-

import re
from idstools.rule import parse_fileobj
from malfeeds.library import get_item_type
from malfeeds.engines import MalFeedEngine
from malfeeds.library import get_clean_item


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


class MalSnortFeed(MalFeedEngine):
    def __init__(self, feedurl, feedtype, **kwargs):
        super(MalSnortFeed, self).__init__(feedurl, feedtype)

    def _stream_iterator(self):
        return self._stream_iterator_http()

    def _update_entries(self):
        rval = True
        ruleslist = parse_fileobj(self._feed_stream.raw)
        for rule in ruleslist:
            rawdata = rule['raw']
            itemslist = extract_itemslist(rawdata)

            for feeditem in itemslist:
                _item = self._struct_entry.copy()
                itype = get_item_type(feeditem)
                _item.update({'type': itype, itype: feeditem})
          #      _item[self._feed_entry_type] = feeditem
                _item['last_update'] = self._feed_header['last_update']
                _item['description'] = rule['msg']
                self._feed_entries.append(_item)
        return rval
