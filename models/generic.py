from google.appengine.ext import ndb


class Base(object):

    @classmethod
    def get_by_key(class_, urlsafe):
        key = ndb.Key(urlsafe=urlsafe)
        return key.get()


class Record(Base):
    name = ndb.StringProperty(indexed=False)
    paragraphs = ndb.TextProperty(repeated=True)

    @property
    def description(self):
        return '\n\n'.join(self.paragraphs)

    @description.setter
    def description(self, value):
        value = value.strip().replace('\r\n', '\n').replace('\r', '\n')
        self.paragraphs = value.split('\n\n')
