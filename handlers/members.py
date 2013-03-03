from .base import BaseHandler

from models.account import User

from webapp2 import Route


class MemberList(BaseHandler):

    templatepath = '/members/list'

    def __init__(self, *args, **kwargs):
        super(MemberList, self).__init__(*args, **kwargs)
        from models.account import Rank
        self.rankmodel = Rank

    def get(self, *args, **kwargs):
        members = {}
        for rank in self.rankmodel.hierarchy():
            query = User.query(User.rankkey == rank.key)
            members[rank.name] = {}
            members[rank.name]['results'] = query
            members[rank.name]['hasmembers'] = query.count(1) > 0

        context = {
            'members': members,
            'hierarchy': self.rankmodel.hierarchy(),
        }
        self.response.out.write(self.loadtemplate(context))


class MemberDetail(BaseHandler):

    templatepath = '/members/profile'

    def get(self, memberkey, *args, **kwargs):
        member = User.getbykey(memberkey)
        context = {
            'member': member,
            }

        self.response.out.write(self.loadtemplate(context))


class MemberFollow(BaseHandler):

    def get(self, memberkey, *args, **kwargs):
        member = User.getbykey(memberkey)
        self.user.following.append(member)
        self.user.put()
        self.redirect('/members/%s' % memberkey)


class MemberUnfollow(BaseHandler):

    def get(self, memberkey, *args, **kwargs):
        member = User.getbykey(memberkey)
        self.user.following.remove(member)
        self.user.put()
        self.redirect('/members/%s' % memberkey)


class GenericMessage(BaseHandler):

    templatepath = '/members/message'

    def __init__(self, *args, **kwargs):
        super(GenericMessage, self).__init__(*args, **kwargs)
        from lib.forms import Message as MessageForm
        self.messageform = MessageForm
        from models.communication import Message as MessageModel
        self.messagemodel = MessageModel

    def render(self, receiver=None, form=None, parent=None):
        if not receiver:
            receiver = parent.sender

        if not form:
            form = self.messageform()

        context = {
            'target': receiver,
            'form': form,
            'parent': parent,
        }

        self.response.out.write(self.loadtemplate(context))

    def makemessage(self, details, target=None, parent=None):
        if not target:
            target = parent.sender

        parentkey = None
        if parent:
            details['subject'] = parent.name
            parentkey = parent.key

        message = self.messagemodel(name=details['subject'],
                                    senderkey=self.user.key,
                                    receiverkey=target.key,
                                    parentkey=parentkey)
        message.description = details['message']
        return message

    def saveform(self, receiver=None, parent=None):
        if not receiver:
            receiver = parent.sender
        form = self.messageform(self.request.params)
        form.validate = True
        if form.isvalid:
            message = self.makemessage(form.cleaneddata,
                                       parent=parent,
                                       target=receiver)
            message.put()
            self.redirect('/members/%s' % receiver.key.urlsafe())
        else:
            return self.render(memberkey, form)


class MemberMessage(GenericMessage):

    def get(self, memberkey):
        target = User.getbykey(memberkey)
        return self.render(receiver=target)

    def post(self, memberkey):
        receiver = User.getbykey(memberkey)
        return self.saveform(receiver=receiver)


class MemberReply(GenericMessage):

    def __init__(self, *args, **kwargs):
        super(MemberReply, self).__init__(*args, **kwargs)
        from lib.forms import Reply as ReplyForm
        self.messageform = ReplyForm

    def get(self, parentkey):
        message = self.messagemodel.getbykey(parentkey)
        return self.render(parent=message)

    def post(self, parentkey):
        message = self.messagemodel.getbykey(parentkey)
        return self.saveform(parent=message)



routes = [
    Route('/', MemberList, name='member-list'),
    Route('/<memberkey>', MemberDetail, name='member-detail'),
    Route('/follow/<memberkey>', MemberFollow, name='member-follow'),
    Route('/unfollow/<memberkey>', MemberUnfollow, name='member-unfollow'),
    Route('/message/<memberkey>', MemberMessage, name='member-message'),
    Route('/reply/<parentkey>', MemberReply, name='member-reply'),
]