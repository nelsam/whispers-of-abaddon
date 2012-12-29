from google.appengine.ext import ndb

from generic import Record

# Note: AppEngine doesn't have any C-level bcrypt libraries, so we
# can't use bcrypt.
#from lib.passlib.hash import pbkdf2_sha512 as authentication


class account(Record):
    login = ndb.StringProperty()
    email = ndb.StringProperty()
    passhash = ndb.StringProperty(indexed=False)

    @classmethod
    def login(model, identifier, password):
        user = model.query(model.login == identifier)
        if not user:
            user = model.query(model.email == identifier)

        if user:
            authed = authentication.verify(password, user.passhash)
            if not authed:
                user = None

        return user
