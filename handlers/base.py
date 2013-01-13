import jinja2
import webapp2
from google.appengine.api import users

import settings

import tarfile


class StaticHandler(webapp2.RequestHandler):

    base_path = '/static/docs'

    def get(self, path, *args, **kwargs):
        import os
        full_path = os.path.join(self.base_path, path)
        if os.path.isfile(full_path):
            static_file = open(full_path, 'r')
            response = static_file.read()
            static_file.close()
            self.response.out.write(response)
        else:
            raise IOError("tarfile loading not implemented yet")


class BaseHandler(webapp2.RequestHandler):

    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        template_loader = jinja2.FileSystemLoader(settings.TEMPLATE_DIR)
        self.environment = jinja2.Environment(loader=template_loader)

    @property
    def parentpath(self):
        return self.levelup(self.request.path)

    @property
    def grandparentpath(self):
        return self.levelup(self.parentpath)

    def levelup(self, path):
        path = path.strip('/')
        endindex = path.rfind('/')
        return '/%s/' % path[:endindex]

    @property
    def templatepath(self):
        from os.path import join
        return join(self.templatedir, self.templatefile)

    @property
    def user(self):
        return self.getuser()

    def getuser(self):
        if hasattr(self, '_user'):
            user = self._user
        else:
            user = users.get_current_user()
            if user:
                from models.account import User
                query = User.query(User.userid == user.user_id())
                user_obj = query.get()
                if user_obj:
                    user = user_obj
                else:
                    # Don't bother to save to the database until they change
                    # some settings.
                    user = User(userid=user.user_id(),
                                email=user.email())

            self._user = user

        return user

    def loadtemplate(self, context={}):      
        templatepath = self.templatepath or self.request.path
        return self._loadtemplate(templatepath=templatepath,
                                  context=context)

    def _loadtemplate(self, templatepath, context={}):
        context['user'] = self.user
        if self.user:
            context['logouturl'] = users.create_logout_url(self.request.path)
        else:
            context['loginurl'] = users.create_login_url(self.request.path)

        templatepath = '%s.jinja2' % templatepath
        template = self.environment.get_template(templatepath)
        return template.render(context)


class List(BaseHandler):

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


class ProcessForm(BaseHandler):

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


class Edit(ProcessForm):

    templatefile = 'edit'

    @property
    def parentpath(self):
        """
        In the edit handler, the parent path will be /edit instead
        of /, because the edit handler requires an item key.  Thus,
        we need to override parentpath to act like grandparentpath,
        so that redirects happen correctly.

        There *is* a better way to do this.
        """
        return self.levelup(self.levelup(self.request.path))

    def get(self, itemkey, *args, **kwargs):
        item = self.model.getbykey(itemkey)
        form = self.form(self.formcontext(item))
        return self.render(form)

    def post(self, itemkey, *args, **kwargs):
        return self.processpost(itemkey)


class Delete(BaseHandler):
    def get(self, itemkey, *args, **kwargs):
        from google.appengine.ext import ndb
        key = ndb.Key(urlsafe=itemkey)
        key.delete()
        self.redirect(self.grandparentpath)