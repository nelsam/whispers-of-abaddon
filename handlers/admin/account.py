from webapp2 import Route
from webapp2_extras import routes

from handlers.admin.base import AdminHandler

from models.account import Rank


class RankBase(AdminHandler):

    templatedir = 'rank'

    def __init__(self, *args, **kwargs):
        super(RankBase, self).__init__(*args, **kwargs)
        from lib.forms import Rank as RankForm
        self.form = RankForm


class RankList(RankBase):

    templatefile = 'list'

    def get(self, *args, **kwargs):
        query = Rank.query().order(Rank.placement)
        context = {
            'ranks': query,
        }
        self.response.out.write(self.loadtemplate(context))


class RankCreate(RankBase):

    templatefile = 'create'

    def get(self, *args, **kwargs):
        return self.render()

    def post(self, *args, **kwargs):
        form = self.form(self.request.params)
        form.validate = True
        if form.isvalid:
            newentry = Rank(
                name=form.cleaneddata['title'],
                placement=form.cleaneddata['placement'])
            newentry.description = form.cleaneddata['body']
            newentry.put()

            self.redirect('/admin/rank/')
        else:
            return self.render(form=form)

    def render(self, form=None):
        if form is None:
            form = self.form()

        context = {
            'form': form,
        }

        self.request.out.write(self.loadtemplate(context))


class RankEdit(RankCreate):

    templatefile = 'edit'

    def get(self, entrykey, *args, **kwargs):
        entry = Rank.get_by_key(entrykey)
        formcontext = {
            'title': entry.name,
            'body': entry.description,
            'placement': entry.placement,
        }
        form = self.form(formcontext)
        return self.render(form)

    def post(self, entrykey, *args, **kwargs):
        form = self.form(self.request.params)
        form.validate = True
        if form.isvalid:
            entry = Record.get_by_key(entrykey)
            entry.name = form.cleaneddata['title']
            entry.description = form.cleaneddata['body']
            entry.placement = form.cleaneddata['placement']
            entry.put()

            self.redirect('/admin/rank/')

        return self.render(form)


class RankDelete(RankBase):

    def get(self, entrykey, *args, **kwargs):
        key = ndb.Key(urlsafe=entrykey)
        key.delete()
        self.redirect('/admin/rank/')


routes = [
    routes.PathPrefixRoute(r'/rank', [
        Route(r'/', RankList, name='admin-rank-list'),
        Route(r'/create', RankCreate, name='admin-rank-create'),
        Route(r'/edit/<entrykey>', RankEdit, name='admin-rank-edit'),
        Route(r'/delete/<entrykey>', RankDelete, name='admin-rank-delete'),
        ]),
]