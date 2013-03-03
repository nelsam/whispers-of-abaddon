# -*- coding: utf-8 -*-

from webapp2 import Route

from ..base import BaseHandler
from models.communication import Message

class Inbox(BaseHandler):

    templatepath = '/account/inbox'

    def get(self):
        messagelist = Message.query(Message.receiverkey == self.user.key)
        messagelist = messagelist.order(-Message.sendtimestamp)

        context = {
            'messages': messagelist,
            }

        self.response.out.write(self.loadtemplate(context))


class MessageView(BaseHandler):

    templatepath = '/account/message'

    def get(self, messagekey):
        message = Message.getbykey(messagekey)
        if not message.read:
            message.read = True
            message.put()

        if not hasattr(self, '_thread'):
            self._thread = []
            parent = message.parent
            while parent is not None and parent not in self._thread:
                self._thread.append(parent)
                parent = parent.parent
            self._thread.reverse()

        context = {
            'message': message,
            'thread': self._thread,
            }

        self.response.out.write(self.loadtemplate(context))


routes = [
    Route('/', Inbox, name='account-inbox'),
    Route('/<messagekey>', MessageView, name='account-message'),
]