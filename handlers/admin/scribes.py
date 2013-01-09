from google.appengine.ext import ndb
from webapp2 import Route

from handlers.admin import base

from models.scribes import OrderedRecord as Record


class Base(base.AdminHandler):

    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)
        self.scribetype = self.request.route_kwargs['scribetype']

        from lib.forms import Record as OrderedRecordForm
        self.form = OrderedRecordForm

        from models.scribes import OrderedRecord as OrderedRecordModel
        self.model = OrderedRecordModel

    @property
    def templatedir(self):
        return self.scribetype


class List(Base, base.List):

    @property
    def query(self):
        return self.model.query(Record.section == self.scribetype)

    @property
    def title(self):
        return '%s Section' % self.scribetype.title()


class Create(Base, base.Create):

    def createitem(self, form):
        newentry = Record(
            section=self.scribetype,
            name=form.cleaneddata['title'])
        newentry.description = form.cleaneddata['body']
        return newentry


class Edit(Base, base.Edit):

    def formcontext(self, item):
        formcontext = {
            'title': item.name,
            'body': item.description,
        }
        return formcontext

    def updateitem(self, item, form):
        item.name = form.cleaneddata['title']
        item.description = form.cleaneddata['body']
        return item


class Delete(Base):

    def get(self, entrykey, *args, **kwargs):
        key = ndb.Key(urlsafe=entrykey)
        key.delete()
        self.redirect('/admin/%s/' % self.scribetype)


routes = [
    Route(r'/', List, name='admin-scribes-list'),
    Route(r'/create', Create, name="admin-lore-create"),
    Route(r'/edit/<itemkey>', Edit, name="admin-lore-edit"),
    Route(r'/delete/<itemkey>', Delete, name="admin-lore-delete"),
]
