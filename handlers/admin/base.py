from handlers.base import BaseHandler, List, Create, Edit, Delete

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

    def loadtemplate(self, context={}):
        templatepath = os.path.join(self._admintemplatedir,
                                    self.templatepath) or self.request.path
        return super(AdminHandler, self)._loadtemplate(templatepath,
                                                       context=context)

