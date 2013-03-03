from google.appengine.ext import ndb
from .generic import Record


class OrderedRecord(Record, ndb.Model):
    section = ndb.StringProperty(required=True)
    rank = ndb.IntegerProperty(default=0)
