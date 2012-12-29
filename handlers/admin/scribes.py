from google.appengine.ext import ndb

from handlers.admin.base import AdminHandler

from models.scribes import OrderedRecord


class lore(object):

    templatedir = 'lore'

    class Base(AdminHandler):

        def __init__(self, *args, **kwargs):
            super(lore.Base, self).__init__(*args, **kwargs)
            from lib.forms import OrderedRecord as OrderedRecordForm
            self.form = OrderedRecordForm

        @property
        def templatepath(self):
            from os.path import join
            return join(lore.templatedir, self.templatefile)

    class List(Base):

        templatefile = 'list'

        def get(self, *args, **kwargs):
            query = OrderedRecord.query(OrderedRecord.section == 'lore')
            lore = query.order(OrderedRecord.rank)

            context = {
                'lore': lore,
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
                newentry = OrderedRecord(
                    section='lore',
                    name=form.cleaneddata['title'])
                newentry.description = form.cleaneddata['body']
                newentry.put()

                self.redirect('/admin/lore')
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
            entry = OrderedRecord.get_by_key(entrykey)
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
                entry = OrderedRecord.get_by_key(entrykey)
                entry.name = form.cleaneddata['title']
                entry.description = form.cleaneddata['body']
                entry.put()

                self.redirect('/admin/lore')

            return self.render(form)

    class Delete(Base):

        def get(self, entrykey, *args, **kwargs):
            key = ndb.Key(urlsafe=entrykey)
            key.delete()
            self.redirect('/admin/lore')