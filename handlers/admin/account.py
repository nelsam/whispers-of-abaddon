from webapp2 import Route
from webapp2_extras import routes

from handlers.admin import base


class AccountMain(base.AdminHandler):

    templatedir = 'account'
    templatefile = 'main'

    def get(self, *args, **kwargs):
        self.response.out.write(self.loadtemplate())


class RankBase(base.AdminHandler):

    templatedir = 'rank'

    def __init__(self, *args, **kwargs):
        super(RankBase, self).__init__(*args, **kwargs)
        from lib.forms import Rank as RankForm
        self.form = RankForm

        from models.account import Rank as RankModel
        self.model = RankModel


class RankList(RankBase, base.List):
    title = 'Rank'


class RankCreate(RankBase, base.Create):

    def createitem(self, form):
        newentry = self.model(
            name=form.cleaneddata['title'],
            placement=form.cleaneddata['placement'])
        newentry.description = form.cleaneddata['body']
        return newentry


class RankEdit(RankBase, base.Edit):

    def formcontext(self, item):
        formcontext = {
            'title': item.name,
            'body': item.description,
            'placement': item.placement,
        }
        return formcontext

    def updateitem(self, item, form):
        item.name = form.cleaneddata['title']
        item.description = form.cleaneddata['body']
        item.placement = form.cleaneddata['placement']
        return item


class RankDelete(RankBase, base.Delete):
    pass


class UserBase(base.AdminHandler):

    templatedir = 'user'

    def __init__(self, *args, **kwargs):
        super(UserBase, self).__init__(*args, **kwargs)
        from models.account import Rank as RankModel
        self.rankmodel = RankModel

        from lib.forms import AdminAccount as UserForm

        def formwrapper(*args, **kwargs):
            userplacement = self.user.rank.placement if self.user.rank else None
            if self.user.hasroot:
                userplacement = -1
            kwargs['maxrank'] = userplacement
            return UserForm(*args, **kwargs)
        self.form = formwrapper

        from models.account import User as UserModel
        self.model = UserModel


class UserList(UserBase, base.List):
    title = 'User'
    create = False


class UserEdit(UserBase, base.Edit):

    def formcontext(self, item):
        rankkey = item.rankkey.urlsafe() if item.rankkey else ''
        formcontext = {
            'name': item.name,
            'about': item.description,
            'isadmin': item.siteadmin,
            'rank': rankkey,
        }
        return formcontext

    def updateitem(self, item, form):
        item.name = form.cleaneddata['name']
        item.description = form.cleaneddata['about']
        item.siteadmin = form.cleaneddata['isadmin']
        item.rank = self.rankmodel.getbykey(form.cleaneddata['rank'])
        return item


class UserDelete(UserBase, base.Delete):
    pass


routes = [
    Route(r'/', AccountMain, name='admin-account-main'),
    routes.PathPrefixRoute(r'/ranks', [
        Route(r'/', RankList, name='admin-rank-list'),
        Route(r'/create', RankCreate, name='admin-rank-create'),
        Route(r'/edit/<itemkey>', RankEdit, name='admin-rank-edit'),
        Route(r'/delete/<itemkey>', RankDelete, name='admin-rank-delete'),
    ]),
    routes.PathPrefixRoute(r'/users', [
        Route(r'/', UserList, name='admin-user-list'),
        Route(r'/edit/<itemkey>', UserEdit, name='admin-user-edit'),
        Route(r'/delete/<itemkey>', UserDelete, name='admin-user-delete'),
    ]),
]