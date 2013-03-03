from google.appengine.ext import ndb

from .generic import Record

import logging


class Profession(Record, ndb.Model):
    pass


class Race(Record, ndb.Model):
    pass


class Discipline(Record, ndb.Model):
    pass


class Character(Record, ndb.Model):
    ownerkey = ndb.KeyProperty(indexed=False)
    professionkey = ndb.KeyProperty(indexed=False)
    racekey = ndb.KeyProperty(indexed=False)
    disciplinekeys = ndb.KeyProperty(repeated=True)
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

    @property
    def owner(self):
        owner = None
        if self.ownerkey:
            owner = self.ownerkey.get()

        return owner

    @owner.setter
    def owner(self, value):
        self.ownerkey = value.key

    @property
    def profession(self):
        profession = None
        if self.professionkey:
            profession = self.professionkey.get()

        return profession

    @profession.setter
    def profession(self, value):
        self.professionkey = value.key

    @property
    def race(self):
        race = None
        if self.racekey:
            race = self.racekey.get()

        return race

    @race.setter
    def race(self, value):
        self.racekey = value.key

    @property
    def disciplines(self):
        disciplines = []
        if self.disciplinekeys:
            disciplines = [key.get() for key in self.disciplinekeys]

        return disciplines

    @disciplines.setter
    def disciplines(self, value):
        self.disciplinekeys = [item.key for item in value]