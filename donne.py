#!/usr/bin/env python

#from maldonne.feeds import MalRssFeed
import ConfigParser
import glob
import os
import sys

def load_feeds():
    base_dir = os.path.dirname(os.path.realpath(__file__))
    feedslist = glob.glob("{0}/feeds/*.ini".format(base_dir))

    try:
        feedsconfig = ConfigParser.ConfigParser()
        feedsconfig.read(feedslist)
    except ConfigParser.ParsingError as e:
        print("error while parsing feeds: {0}".format(e))

    for section in feedsconfig.sections():
        if feedsconfig.getint(section, "enabled") != 0:
            feedsconfig.remove_section(section)
    
    return feedsconfig
    

def main():
    f = load_feeds()
    print f.sections()
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
