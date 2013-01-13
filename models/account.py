from google.appengine.ext import ndb
from google.appengine.api import users

from generic import Record


class Rank(Record, ndb.Model):
    placement = ndb.IntegerProperty()

    @classmethod
    def hierarchy(class_, minrank=None, maxrank=None):
        query = class_.query()
        if minrank is not None:
            query = query.filter(class_.placement <= minrank)

        if maxrank is not None:
            query = query.filter(class_.placement >= maxrank)

        query = query.order(class_.placement)
        return query

class User(Record, ndb.Model):
    userid = ndb.StringProperty()
    email = ndb.StringProperty(indexed=False)
    characterkeys = ndb.KeyProperty(repeated=True)
    rankkey = ndb.KeyProperty()
    siteadmin = ndb.BooleanProperty(default=False)

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
        rank = None
        if self.rankkey:
            rank = self.rankkey.get()

        return rank

    @rank.setter
    def rank(self, rank):
        self.rankkey = rank.key

    @property
    def hasroot(self):
        return self.siteadmin or users.is_current_user_admin()

    def put(self, *args, **kwargs):
        if hasattr(self, '_characters'):
            self.characterkeys = [char.key for char in self._characters]

        super(User, self).put(*args, **kwargs)