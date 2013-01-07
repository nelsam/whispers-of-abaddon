from google.appengine.ext import ndb
from webapp2 import Route

from handlers.admin.base import AdminHandler

from models.scribes import OrderedRecord as Record


class Base(AdminHandler):

    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)
        self.scribetype = self.request.route_kwargs['scribetype']
        from lib.forms import Record as OrderedRecordForm
        self.form = OrderedRecordForm

    @property
    def templatedir(self):
        return self.scribetype


class List(Base):

    templatefile = 'list'

    def get(self, *args, **kwargs):
        import logging
        logging.info("Loading scribes of type %s" % self.scribetype)
        query = Record.query(Record.section == self.scribetype)
        entries = query.order(Record.rank)

        context = {
            'records': entries,
        }

        self.response.out.write(self.loadtemplate(context))


class Create(Base):

    templatefile = 'create'

    def get(self, *args, **kwargs):
        return self.render()

    def post(self, *args, **kwargs):
        form = self.form(self.request.params)
        form.validate = True
        if form.isvalid:
            newentry = Record(
                section=self.scribetype,
                name=form.cleaneddata['title'])
            newentry.description = form.cleaneddata['body']
            newentry.put()

            self.redirect('/admin/%s/' % self.scribetype)
        else:
            return self.render(form=form)

    def render(self, form=None):
        if form is None:
            form = self.form()

        context = {
            'form': form,
        }

        self.response.out.write(self.loadtemplate(context))


class Edit(Create):

    def get(self, entrykey, *args, **kwargs):
        entry = Record.get_by_key(entrykey)
        formcontext = {
            'title': entry.name,
            'body': entry.description,
        }
        form = self.form(formcontext)
        return self.render(form)

    def post(self, entrykey, *args, **kwargs):
        form = self.form(self.request.params)
        form.validate = True
        if form.isvalid:
            entry = Record.get_by_key(entrykey)
            entry.name = form.cleaneddata['title']
            entry.description = form.cleaneddata['body']
            entry.put()

            self.redirect('/admin/%s/' % self.scribetype)

        return self.render(form)


class Delete(Base):

    def get(self, entrykey, *args, **kwargs):
        key = ndb.Key(urlsafe=entrykey)
        key.delete()
        self.redirect('/admin/%s/' % self.scribetype)


routes = [
    Route(r'/', List, name='admin-scribes-list'),
    Route(r'/create', Create, name="admin-lore-create"),
    Route(r'/edit/<entrykey>', Edit, name="admin-lore-edit"),
    Route(r'/delete/<entrykey>', Delete, name="admin-lore-delete"),
]
