#!/usr/bin/env python

from malfeeds.objects import MalFeedsCollection, MalFeed
import ConfigParser
import glob
import os
import sys

# dev mode baby :p
from pprint import pprint


class MalFeedsFactory(object):
    def __init__(self, conffile=None, enabled_feeds=False):
        self.feedsconfig = self.load_config(conffile, enabled_feeds)

    def load_config(self, conffile=None, enabled_feeds=False):
        feedsconfig = None
        if conffile is not None:
            feedsconfig = self._config_parser([conffile], enabled_feeds)
        return feedsconfig

    def _config_parser(self, feedslist, enabled_feeds=False):
        try:
            feedsconfig = ConfigParser.ConfigParser()
            feedsconfig.read(feedslist)
        except ConfigParser.ParsingError as e:
            print("error while parsing feeds: {0}".format(e))

        for section in feedsconfig.sections():
            if enabled_feeds is True and feedsconfig.getint(section, "enabled") == 0:
                feedsconfig.remove_section(section)
            else:
                feedsconfig.set(section, "name", section)

        return feedsconfig

    def create_collection(self):
        mfcollection = MalFeedsCollection()

        for section in self.feedsconfig.sections():
            mfsection = dict(self.feedsconfig.items(section))
            try:
                _mf = MalFeed(mfsection)
                mfcollection.add(_mf)
            except Exception, e:
                print("error while creating malfeed: {0}".format(str(e)))

        return mfcollection
