from google.appengine.ext import ndb
from generic import individual


class profession(ndb.Model):
    name = ndb.StringProperty(indexed=False)


class character(individual):
    profession = ndb.KeyProperty(indexed=False)
