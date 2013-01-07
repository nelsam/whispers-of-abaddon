from google.appengine.ext import ndb
from generic import Record


class Record(Record, ndb.Model):
    section = ndb.StringProperty()
    rank = ndb.IntegerProperty()
