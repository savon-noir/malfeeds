#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
from pprint import pprint
from malfeedsfactory import MalFeedsFactory


class TestAV(unittest.TestCase):
    def setUp(self):
        self._rootdir = os.path.dirname(os.path.realpath(__file__))
        print self._rootdir
        feedsfactory = MalFeedsFactory(conffile='{0}/feeds/alienvault.ini'.format(self._rootdir))
        self.mfcollection = feedsfactory.create_collection()
        print self.mfcollection

    def test_av_base(self):
        print self.mfcollection.list()
        for malfeed in self.mfcollection.list():
            if malfeed.enabled:
                malfeed.update()
                pprint(malfeed.name)
                pprint(malfeed.feed_header)
                print "_________________________"
    #        manipulate the objects (not like below)
    #        print malfeed.header()
                for mentry in malfeed.feed_entries:
                    pprint(mentry)
                    print "---------------------"
                print "========================"

if __name__ == '__main__':
    test_suite = ['test_av_base']
    suite = unittest.TestSuite(map(TestAV, test_suite))
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)
