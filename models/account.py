from google.appengine.ext import ndb

from generic import Record


class Rank(Record, ndb.Model):
    placement = ndb.IntegerProperty()

    @classmethod
    def hierarchy(cls):
        return cls.query().order(cls.placement)

class User(Record, ndb.Model):
    userid = ndb.StringProperty()
    email = ndb.StringProperty(indexed=False)
    characterkeys = ndb.KeyProperty(repeated=True)
    rankkey = ndb.KeyProperty()

    @property
    def characters(self):
        return [charkey.get() for charkey in self.characterkeys]

    @characters.setter
    def characters(self, charlist):
        self.characterkeys = [char.key for char in charlist]

    @property
    def rank(self):
        return self.rankkey.get()

    @rank.setter
    def rank(self, rank):
        self.rankkey = rank.key()
