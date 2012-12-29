import jinja2
import webapp2

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

  def loadtemplate(self, context={}):
    templatepath = self.templatepath or self.request.path
    return self._loadtemplate(templatepath=templatepath,
                              context=context)

  def _loadtemplate(self, templatepath, context={}):
    context['member_ranks'] = ['leaders', 'officers', 'members']

    templatepath = '%s.jinja2' % templatepath
    template = self.environment.get_template(templatepath)
    return template.render(context)
