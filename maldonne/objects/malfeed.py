# -*- coding: utf-8 -*-


class MalFeed(object):
    def __init__(self, malengine, malfeedconfig):
        self.name = malfeedconfig.get('name', None)
        self.engine = malfeedconfig.get('engine', None)
        self.feedurl = malfeedconfig.get('feedurl', None)
        self.tags = malfeedconfig.get('tags', '')
        self.threat = malfeedconfig.get('threat', 'unknown')
        self.type = malfeedconfig.get('url', 'unknown')
        self.use_dns = malfeedconfig.get('use_dns', 0)
        self.use_geoip = malfeedconfig.get('use_geoip', 0)

        self.synced = 0
        self.uptodate = 0

        self.items = []

        if None in [self.name, self.engine, self.feedurl]:
            raise Exception("Error: failed to instanciate MalFeed class. "
                            "Verify required parameters in .ini file")

        self._engine = malengine

    def update(self):
        self._engine.update()

    def header(self):
        return self._engine.feed_header

    def entries(self):
        return self._engine.feed_entries
