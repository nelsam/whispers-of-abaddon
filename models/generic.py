from google.appengine.ext import ndb


class individual(ndb.Model):
    name = ndb.StringProperty(indexed=False)
    description = ndb.TextProperty()
