# -*- coding: utf-8 -*-

from models.communication import Forum
from handlers.admin import base

from lib.forms import Forum as ForumForm


class ForumBase(base.AdminHandler):
    templatedir = 'forums'

    def __init__(self, *args, **kwargs):
        super(ForumBase, self).__init__(*args, **kwargs)
        self.form = ForumForm
        self.model = Forum


class ForumList(ForumBase, base.List):
    title = 'Forum'


class ForumCreate(ForumBase, base.Create):

    def createitem(self, form):
        newentry = self.model(name=form.cleaneddata["title"],
                              viewlevel=form.cleaneddata["viewlevel"],
                              replylevel=form.cleaneddata["replylevel"],
                              newthreadlevel=form.cleaneddata["newthreadlevel"])
        newentry.description = form.cleaneddata['body']
        return newentry


class ForumEdit(ForumBase, base.Edit):

    def formcontext(self, item):
        formcontext = {
            'title': item.name,
            'body': item.description,
            'viewlevel': item.viewlevel,
            'replylevel': item.replylevel,
            'newthreadlevel': item.newthreadlevel,
        }
        return formcontext

    def updateitem(self, item, form):
        item.name = form.cleaneddata['title']
        item.viewlevel = form.cleaneddata['viewlevel']
        item.replylevel = form.cleaneddata['replylevel']
        item.newthreadlevel = form.cleaneddata['newthreadlevel']
        item.description = form.cleaneddata['body']
        return item


class ForumDelete(ForumBase, base.Delete):
    pass
