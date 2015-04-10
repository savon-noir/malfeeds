#!/usr/bin/env python

from malfeeds.objects import MalFeedsCollection, MalFeed
import ConfigParser
import glob
import os
import sys

# dev mode baby :p
from pprint import pprint


class MalFeedsFactory(object):
    def __init__(self, confdir=None, enabled_feeds=False):
        self.feedsconfig = self.load_configs(confdir, enabled_feeds)

    def load_config(self, conffile=None, enabled_feeds=False):
        feedsconfig = None
        if conffile is not None:
            feedsconfig = self._config_parser([conffile], enabled_feeds)
        return feedsconfig

    def load_configs(self, confdir=None, enabled_feeds=False):
        if confdir is not None:
            base_dir = confdir
        else:
            base_dir = os.path.dirname(os.path.realpath(__file__)) + '/feeds/'
        feedslist = glob.glob("{0}/*.ini".format(base_dir))

        feedsconfig = self._config_parser(feedslist, enabled_feeds)
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
            mfcollection.add(MalFeed(mfsection))

        return mfcollection


def main():
    feedsfactory = MalFeedsFactory()
    mfcollection = feedsfactory.create_collection()
    for malfeed in mfcollection.list():
        if malfeed.enabled:
            malfeed.update()
            pprint(malfeed.name)
            pprint(malfeed.header())
            print "_________________________"
#        manipulate the objects (not like below)
#        print malfeed.header()
            for mentry in malfeed.entries():
                pprint(mentry)
                print "---------------------"
            print "========================"


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
