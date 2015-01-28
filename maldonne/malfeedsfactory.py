#!/usr/bin/env python

from maldonne.objects import MalFeedsCollection, MalFeed
import inspect
import ConfigParser
import glob
import os
import sys


class MalFeedsFactory(object):
    def __init__(self, confdir=None):
        self.feedsconfig = self.load_configs()

    def load_configs(self, confdir=None):
        if confdir is not None:
            base_dir = confdir
        else:
            base_dir = os.path.dirname(os.path.realpath(__file__))

        feedslist = glob.glob("{0}/feeds/*.ini".format(base_dir))
        print feedslist

        try:
            feedsconfig = ConfigParser.ConfigParser()
            feedsconfig.read(feedslist)
        except ConfigParser.ParsingError as e:
            print("error while parsing feeds: {0}".format(e))

        for section in feedsconfig.sections():
            if feedsconfig.getint(section, "enabled") == 0:
                feedsconfig.remove_section(section)
            else:
                feedsconfig.set(section, "name", section)

        return feedsconfig

    def load_engine(self, feedconfig):
        engineobj = None
        engine_name = feedconfig.get('engine', 'rssmalfeed')
        engine_path = "maldonne.engines.{0}".format(engine_name)
        __import__(engine_path)
        engine_module = sys.modules[engine_path]
        engine_classes = inspect.getmembers(engine_module, inspect.isclass)

        classname, classproxy = engine_classes.pop()
        if inspect.getmodule(classproxy).__name__.find(engine_path) == 0:
            try:
                engineobj = classproxy(feedconfig)
            except Exception as error:
                raise Exception("Cannot create engine, unexpected engine name: {0}".format(error))
        return engineobj

    def get_feeds(self):
        mfcollection = MalFeedsCollection()

        for section in self.feedsconfig.sections():
            mfsection = dict(self.feedsconfig.items(section))
            mfengine = self.load_engine(mfsection)
            mfcollection.add(MalFeed(mfengine, mfsection))

        return mfcollection


def main():
    feedsfactory = MalFeedsFactory()
    for malfeed in feedsfactory.get_feeds():
        print malfeed.name
        malfeed.update()
        print malfeed.header()
        print "-----------------------------"


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
