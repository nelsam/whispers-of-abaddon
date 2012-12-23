import jinja2

class BaseHandler(webapp2.RequestHandler):

    def __init__(self, *args, **kwargs):
        super(BaseResponse, self).__init__(*args, **kwargs)
        template_loader = jinja2.FileSystemLoader(settings.TEMPLATE_DIR)
        self.environment = jinja2.Environment(loader=template_loader)

    def loadtemplate(self, context={}):
        template = '%s.jinja2' % (self.template_path or self.request.path)
        template = self.environment.get_template(path)
        return template.render(context)
