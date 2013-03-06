from google.appengine.ext import ndb
from google.appengine.api import users

from .generic import Record


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
    followingkeys = ndb.KeyProperty(repeated=True)

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

    @property
    def unreadmessages(self):
        if not hasattr(self, '_unread'):
            if not hasattr(self, '_messagemodel'):
                from .communication import Message
                self._messagemodel = Message
            receiverfilter = self._messagemodel.receiverkey
            readfilter = self._messagemodel.read
            unreadquery = self._messagemodel.query(receiverfilter == self.key,
                                                   readfilter == False)
            self._unread = unreadquery.count(50)
        return self._unread

    @property
    def messages(self):
        if not hasattr(self, '_messages'):
            if not hasattr(self, '_messagemodel'):
                from communication import Message
                self._messagemodel = Message
            self._messages = self._messagemodel.query(receiverkey == self.key)
        return self._messages

    @property
    def following(self):
        if not hasattr(self, '_following'):
            self._following = [key.get() for key in self.followingkeys]

        return self._following

    @following.setter
    def following(self, value):
        self._following = value
        self.followingkeys = [item.key for item in value]

    def isfollowing(self, target):
        """
        Check if this user is following a target user.
        """
        return target.key in self.followingkeys

    def put(self, *args, **kwargs):
        if hasattr(self, '_characters'):
            self.characterkeys = [char.key for char in self._characters]

        if hasattr(self, '_following'):
            self.followingkeys = [following.key for
                                  following in self._following]

        super(User, self).put(*args, **kwargs)