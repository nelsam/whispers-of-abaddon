from base import BaseHandler

class Home(BaseHandler):

    template_path = 'simple/home'

    def get(self, *args, **kwargs):
        self.response.out.write(self.loadtemplate())
