from handlers.base import BaseHandler

import os

from google.appengine.api import users


class AdminHandler(BaseHandler):

    _admintemplatedir = 'admin'

    def __init__(self, *args, **kwargs):
        if not (self.user.siteadmin or
                users.is_current_user_admin()):
            self.redirect('/')
        else:
            super(AdminHandler, self).__init__(*args, **kwargs)

    @property
    def parentpath(self):
        path = self.request.path.strip('/')
        endindex = path.rfind('/')
        return '/%s/' % path[:endindex]

    @property
    def templatepath(self):
        from os.path import join
        return join(self.templatedir, self.templatefile)

    def loadtemplate(self, context={}):
        templatepath = os.path.join(self._admintemplatedir,
                                    self.templatepath) or self.request.path
        return super(AdminHandler, self)._loadtemplate(templatepath,
                                                       context=context)


class List(AdminHandler):

    templatefile = 'list'

    create = True
    edit = True
    delete = True

    @property
    def query(self):
        return self.model.query()

    def get(self, *args, **kwargs):
        context = {
            'records': self.query,
            'title': self.title,
            'basepath': self.request.path.strip('/'),
            'create': self.create,
            'edit': self.edit,
            'delete': self.delete,
        }
        self.response.out.write(self.loadtemplate(context))


class ProcessForm(AdminHandler):

    def processpost(self, itemkey=None):
        form = self.form(self.request.params)
        form.validate = True
        if form.isvalid:
            if itemkey:
                item = self.model.getbykey(itemkey)
                self.updateitem(item, form)
                item.put()
            else:
                item = self.createitem(form)
                item.put()
            self.redirect(self.parentpath)
        else:
            return self.render(form)

    def render(self, form=None):
        if form is None:
            form = self.form()

        context = {
            'form': form,
        }
        self.response.out.write(self.loadtemplate(context))


class Create(ProcessForm):

    templatefile = 'create'

    def get(self, *args, **kwargs):
        return self.render()

    def post(self, *args, **kwargs):
        return self.processpost()


class Edit(Create):

    templatefile = 'edit'

    def get(self, itemkey, *args, **kwargs):
        item = self.model.getbykey(itemkey)
        form = self.form(self.formcontext(item))
        return self.render(form)

    def post(self, itemkey, *args, **kwargs):
        return self.processpost(itemkey)


class Delete(AdminHandler):
    def get(self, itemkey, *args, **kwargs):
        from google.appengine.ext import ndb
        key = ndb.Key(urlsafe=itemkey)
        key.delete()
        self.redirect(self.parentpath)