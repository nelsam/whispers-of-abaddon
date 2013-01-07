from handlers.base import BaseHandler

import os


class AdminHandler(BaseHandler):

    _admintemplatedir = 'admin'

    @property
    def templatepath(self):
        from os.path import join
        return join(self.templatedir, self.templatefile)

    def loadtemplate(self, context={}):
        templatepath = os.path.join(self._admintemplatedir,
                                    self.templatepath) or self.request.path
        return super(AdminHandler, self)._loadtemplate(templatepath,
                                                       context=context)