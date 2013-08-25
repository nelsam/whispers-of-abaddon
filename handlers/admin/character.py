from webapp2 import Route
from webapp2_extras import routes

from handlers.admin import base


class CharacterMain(base.AdminHandler):

    templatedir = 'character'
    templatefile = 'main'

    def get(self, *args, **kwargs):
        self.response.out.write(self.loadtemplate())


class ProfessionBase(base.AdminHandler):

    templatedir = 'profession'

    def __init__(self, *args, **kwargs):
        super(ProfessionBase, self).__init__(*args, **kwargs)
        from lib.forms import Record as RecordForm
        self.form = RecordForm

        from models.character import Profession as ProfessionModel
        self.model = ProfessionModel


class ProfessionList(ProfessionBase, base.List):
    title = 'Profession'


class ProfessionCreate(ProfessionBase, base.Create):

    def createitem(self, form):
        newentry = self.model(name=form.cleaneddata['title'])
        newentry.description = form.cleaneddata['body']
        return newentry


class ProfessionEdit(ProfessionBase, base.Edit):

    def formcontext(self, item):
        formcontext = {
            'title': item.name,
            'body': item.description,
        }
        return formcontext

    def updateitem(self, item, form):
        item.name = form.cleaneddata['title']
        item.description = form.cleaneddata['body']
        return item


class ProfessionDelete(ProfessionBase, base.Delete):
    pass


class RaceBase(base.AdminHandler):

    templatedir = 'race'

    def __init__(self, *args, **kwargs):
        super(RaceBase, self).__init__(*args, **kwargs)
        from lib.forms import Record as RecordForm
        self.form = RecordForm

        from models.character import Race as RaceModel
        self.model = RaceModel


class RaceList(RaceBase, base.List):
    title = 'Race'


class RaceCreate(RaceBase, base.Create):

    def createitem(self, form):
        newentry = self.model(name=form.cleaneddata['title'])
        newentry.description = form.cleaneddata['body']
        return newentry


class RaceEdit(RaceBase, base.Edit):

    def formcontext(self, item):
        formcontext = {
            'title': item.name,
            'body': item.description,
        }
        return formcontext

    def updateitem(self, item, form):
        item.name = form.cleaneddata['title']
        item.description = form.cleaneddata['body']
        return item


class RaceDelete(RaceBase, base.Delete):
    pass


class DisciplineBase(base.AdminHandler):

    templatedir = 'discipline'

    def __init__(self, *args, **kwargs):
        super(DisciplineBase, self).__init__(*args, **kwargs)
        from lib.forms import Record as RecordForm
        self.form = RecordForm

        from models.character import Discipline as DisciplineModel
        self.model = DisciplineModel


class DisciplineList(DisciplineBase, base.List):
    title = 'Discipline'


class DisciplineCreate(DisciplineBase, base.Create):

    def createitem(self, form):
        newentry = self.model(name=form.cleaneddata['title'])
        newentry.description = form.cleaneddata['body']
        return newentry


class DisciplineEdit(DisciplineBase, base.Edit):

    def formcontext(self, item):
        formcontext = {
            'title': item.name,
            'body': item.description,
        }
        return formcontext

    def updateitem(self, item, form):
        item.name = form.cleaneddata['title']
        item.description = form.cleaneddata['body']
        return item


class DisciplineDelete(DisciplineBase, base.Delete):
    pass


routes = [
    Route(r'/', CharacterMain, name='admin-character-main'),
    routes.PathPrefixRoute(r'/profession', [
        Route(r'/', ProfessionList, name='admin-profession-list'),
        Route(r'/create', ProfessionCreate, name='admin-profession-create'),
        Route(r'/edit/<itemkey>', ProfessionEdit, name='admin-profession-edit'),
        Route(r'/delete/<itemkey>', ProfessionDelete,
              name='admin-profession-delete'),
    ]),
    routes.PathPrefixRoute(r'/race', [
        Route(r'/', RaceList, name='admin-race-list'),
        Route(r'/create', RaceCreate, name='admin-race-create'),
        Route(r'/edit/<itemkey>', RaceEdit, name='admin-race-edit'),
        Route(r'/delete/<itemkey>', RaceDelete, name='admin-race-delete'),
    ]),
    routes.PathPrefixRoute(r'/discipline', [
        Route(r'/', DisciplineList, name='admin-discipline-list'),
        Route(r'/create', DisciplineCreate, name='admin-discipline-create'),
        Route(r'/edit/<itemkey>', DisciplineEdit, name='admin-discipline-edit'),
        Route(r'/delete/<itemkey>', DisciplineDelete,
              name='admin-discipline-delete'),
    ]),
]