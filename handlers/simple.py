from base import BaseHandler


class Home(BaseHandler):

    templatepath = 'simple/home'

    def get(self, *args, **kwargs):
        self.response.out.write(self.loadtemplate())


class Section(object):
    title = None
    description = None

    def __init__(self):
        self.description = []


class Scribes(BaseHandler):

    @property
    def query(self):
        from models.scribes import OrderedRecord
        query = OrderedRecord.query(OrderedRecord.section == self.scribetype)
        records = query.order(OrderedRecord.rank)

        return records

    def get(self, *args, **kwargs):
        context = {
            'records': self.query,
        }
        self.response.out.write(self.loadtemplate(context))


class Lore(Scribes):
    
    templatepath = 'simple/lore'
    scribetype = 'lore'

class About(Scribes):

    templatepath = 'simple/about'
    scribetype = 'about'

