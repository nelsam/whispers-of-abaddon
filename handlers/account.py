from base import BaseHandler

from webapp2 import Route


class Account(BaseHandler):

    templatepath = '/account/main'

    def get(self, *args, **kwargs):
        self.response.out.write(self.loadtemplate())


class AccountEdit(BaseHandler):

    templatepath = '/account/edit'

    def __init__(self, *args, **kwargs):
        super(AccountEdit, self).__init__(*args, **kwargs)
        from lib.forms import Account as AccountForm
        self.form = AccountForm

    def get(self, *args, **kwargs):
        return self.render()

    def post(self, *args, **kwargs):
        form = self.form(self.request.params)
        form.validate = True
        if form.isvalid:
            self.user.name = form.cleaneddata['name']
            self.user.description = form.cleaneddata['about']
            self.user.put()
            self.redirect('/account/')
        else:
            return self.render(form=form)

    def render(self, form=None):
        if form is None:
            user_context = {
                'name': self.user.name,
                'about': self.user.description,
            }
            form = self.form(user_context)

        context = {
            'form': form,
        }

        self.response.out.write(self.loadtemplate(context))


routes = [
    Route('/', Account, name='account'),
    Route('/edit', AccountEdit, name='account-edit'),
]