# -*- coding: utf-8 -*-

import hashlib
import inspect
import sys
from malfeeds.objects.malfeedentry import MalFeedEntry


class MalFeed(object):
    def __init__(self, malfeedconfig):
        self.name = malfeedconfig.get('name', None)
        self.title = malfeedconfig.get('title', '')
        self.description = malfeedconfig.get('description', '')
        self.publisher = malfeedconfig.get('publisher', '')
        self.rights = malfeedconfig.get('rights', '')

        self.engine_name = malfeedconfig.get('engine', None)
        self.feedurl = malfeedconfig.get('feedurl', None)
        self.tags = malfeedconfig.get('tags', '').split(',')
        self.type = malfeedconfig.get('type', None)
        self.input_type = malfeedconfig.get('input_type', None)
        self.threat = malfeedconfig.get('threat', 'unknown')
        self.confidence = malfeedconfig.get('confidence', 0)
        self.use_dns = int(malfeedconfig.get('use_dns', 0))
        self.use_geoip = int(malfeedconfig.get('use_geoip', 0))
        self.extended = int(malfeedconfig.get('extended', 0))

        self.create_date = None
        self.last_update = None
        self.last_status = None

        self.id = hashlib.md5(self.feedurl).hexdigest()

        self.synced = 0
        self.uptodate = 0
        self.enabled = int(malfeedconfig.get('enabled', 0))

        extra_list = ['comment', 'pattern', 'delimiter']
        self._engine_extra = dict((k, malfeedconfig[k]) for k in extra_list if k in malfeedconfig.keys())

        self._entries = []

        self._engine = self._load_engine(self.engine_name)
        if None in [self.name, self.engine_name, self.feedurl, self.type, self._engine]:
            raise Exception("Error: failed to instanciate MalFeed class. "
                            "Verify required parameters in .ini file")

    def update(self):
        self._engine.update()
        self._update_header()

    def _update_header(self):
        fh = self._engine.feed_header
        for hk in fh.keys():
            oattr = getattr(self, hk)
            if oattr is None or len(oattr) == 0:
                setattr(self, hk, fh[hk])

    @property
    def feed_entries(self):
        for eentry in self._engine.feed_entries:
            eentry.update({'tags': self.tags,
                           'feedurl': self.feedurl,
                           'type': self.type})
            yield MalFeedEntry(eentry, self.extended)

    @property
    def feed_header(self):
        rh = dict(self.__dict__)
        del rh['_entries']
        del rh['_engine']
        return rh

    def _load_engine(self, engine_name):
        engineobj = None
        engine_path = "malfeeds.engines.{0}".format(engine_name)
        __import__(engine_path)
        engine_module = sys.modules[engine_path]
        engine_classes = inspect.getmembers(engine_module, inspect.isclass)

        for engine_classe in engine_classes:
            classname, classproxy = engine_classe
            if classname != 'MalFeedEngine':
                break
        if inspect.getmodule(classproxy).__name__.find(engine_path) == 0:
            try:
                engineobj = classproxy(self.feedurl, self.type, self.input_type, **self._engine_extra)
            except Exception as error:
                raise Exception("Cannot create engine {0}, unexpected engine name: {1}".format(engine_name, error))
        return engineobj

    def __str__(self):
        return str(self.__dict__)
