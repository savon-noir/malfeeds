# -*- coding: utf-8 -*-

class MalFeed(object):
    def __init__(self, malfeedconfig):
        self.engine = malfeedconfig.get('engine', None)
        self.feedurl = malfeedconfig.get('feedurl', None)
        self.tags = malfeedconfig.get('tags', '')
        self.threat = malfeedconfig.get('threat', 'unknown')
        self.type = malfeedconfig.get('url', 'unknown')

        self.synced = 0
        self.uptodate = 0

        self.items = []
