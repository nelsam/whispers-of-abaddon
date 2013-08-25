import datetime

from google.appengine.ext import ndb

from .generic import Record


class BaseMessage(Record, ndb.Model):
    senderkey = ndb.KeyProperty(required=True)
    sendtimestamp = ndb.DateTimeProperty(auto_now_add=True)

    @property
    def sender(self):
        if not hasattr(self, '_sender'):
            self._sender = self.senderkey.get()

        return self._sender


class Message(BaseMessage, ndb.Model):
    receiverkey = ndb.KeyProperty(required=True)
    read = ndb.BooleanProperty(default=False)
    parentkey = ndb.KeyProperty(required=False)

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


class ForumThread(BaseMessage):
    forum = ndb.KeyProperty(required=True)
    updated = ndb.DateTimeProperty(auto_now_add=True)


class ForumMessage(BaseMessage):
    thread = ndb.KeyProperty(required=True)

    def put(self, *args, **kwargs):
        """
        Set the update dates.
        """
        now = datetime.datetime.now()
        if self.thread:
            self.thread.updated = now
            self.thread.put()
        self.sendtimestamp = now
        super(ForumMessage, self).put(*args, **kwargs)
