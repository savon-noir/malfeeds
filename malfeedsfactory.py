#!/usr/bin/env python

#from maldonne.feeds import MalRssFeed
import ConfigParser
import glob
import os
import sys

class MalFeedsFactory(object):
    def __init__(self):
        self.feedsconfig = self.load_feeds()
        self.malfeeds = [] #MalFeedsCollection()
        
    def load_feeds(self):
        base_dir = os.path.dirname(os.path.realpath(__file__))
        feedslist = glob.glob("{0}/feeds/*.ini".format(base_dir))
    
        try:
            feedsconfig = ConfigParser.ConfigParser()
            feedsconfig.read(feedslist)
        except ConfigParser.ParsingError as e:
            print("error while parsing feeds: {0}".format(e))
    
        for section in feedsconfig.sections():
            print dict(feedsconfig.items(section))
            if feedsconfig.getint(section, "enabled") != 0:
                feedsconfig.remove_section(section)
 
        return feedsconfig
    
    def get_feed_header(feedname):
        return self.malfeeds[feedname].header

    def get_feed_entries(feedname):
        return self.malfeeds[feedname].entries

def main():
    mfactory = MalFeedsFactory()
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
