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
    siteadmin = ndb.BooleanProperty()

    @property
    def characters(self):
        if not hasattr(self, '_characters'):
            self._characters = [charkey.get() for charkey in self.characterkeys]
        return self._characters

    @characters.setter
    def characters(self, charlist):
        self._characters = charlist
        self.characterkeys = [char.key for char in charlist]

    @property
    def rank(self):
        return self.rankkey.get()

    @rank.setter
    def rank(self, rank):
        self.rankkey = rank.key()

    def put(self, *args, **kwargs):
        if hasattr(self, '_characters'):
            self.characterkeys = [char.key for char in self._characters]

        super(User, self).put(*args, **kwargs)