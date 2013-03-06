from google.appengine.ext import ndb

from .generic import Record


class Message(Record, ndb.Model):
    senderkey = ndb.KeyProperty(required=True)
    receiverkey = ndb.KeyProperty(required=True)
    sendtimestamp = ndb.DateTimeProperty(auto_now_add=True)
    read = ndb.BooleanProperty(default=False)
    parentkey = ndb.KeyProperty(required=False)

    @property
    def sender(self):
        if not hasattr(self, '_sender'):
            self._sender = self.senderkey.get()

        return self._sender

    @property
    def receiver(self):
        if not hasattr(self, '_receiver'):
            self._receiver = self.receiverkey.get()

        return self._receiver

    @property
    def parent(self):
        if not hasattr(self, '_parent'):
            if self.parentkey:
                self._parent = self.parentkey.get()
            else:
                self._parent = None

        return self._parent

    @property
    def summary(self):
        if not hasattr(self, '_summary'):
            self._summary = self.description[:150]

        return self._summary


class Forum(Record, ndb.Model):
    viewlevel = ndb.IntegerProperty(required=True)
    replylevel = ndb.IntegerProperty(required=True)
    newthreadlevel = ndb.IntegerProperty(required=True)

    def usercanview(self, user):
        return user.rank.placement <= self.viewlevel

    def usercanreply(self, user):
        return user.rank.placement <= self.replylevel

    def usercancreatethreads(self, user):
        return user.rank.placement <= self.newthreadlevel


class ForumThread(Message):
    forum = ndb.KeyProperty(required=True)