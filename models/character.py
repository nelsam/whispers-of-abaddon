from google.appengine.ext import ndb
from generic import Record

import logging


class Profession(Record, ndb.Model):
    pass


class Race(Record, ndb.Model):
    pass


class Discipline(Record, ndb.Model):
    pass


class character(Record, ndb.Model):
    profession = ndb.KeyProperty(indexed=False)
    race = ndb.KeyProperty(indexed=False)
    disciplines = ndb.KeyProperty(repeated=True)
    leveldata = ndb.IntegerProperty(default=1)

    @property
    def level(self):
        if self.leveldata > 80 or self.leveldata < 1:
            self.leveldata = 1
            logging.warning("Invalid value stored for level data; reset to 1.")
        else:
            return self.leveldata

    @level.setter
    def level(self, value):
        if value > 80 or value < 1:
            raise IOError("Invalid value for level data passed")
        else:
            self.leveldata = value
