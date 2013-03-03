# -*- coding: utf-8 -*-

from webapp2 import Route

from ..base import BaseHandler, Create, Edit, Delete


class CharacterBase(BaseHandler):

    templatedir = '/account/character'

    def __init__(self, *args, **kwargs):
        super(CharacterBase, self).__init__(*args, **kwargs)
        from lib.forms import Character as CharacterForm
        self.form = CharacterForm

        import models.character as charmodels
        self.model = charmodels.Character
        self.professionmodel = charmodels.Profession
        self.racemodel = charmodels.Race
        self.disciplinemodel = charmodels.Discipline


class CharacterHome(CharacterBase):

    def get(self, *args, **kwargs):
        self.redirect('/account/')


class CharacterCreate(CharacterBase, Create):

    def createitem(self, form):
        professionkey = form.cleaneddata['profession']
        profession = self.professionmodel.getbykey(professionkey)

        racekey = form.cleaneddata['race']
        race = self.racemodel.getbykey(racekey)

        discipline1key = form.cleaneddata['discipline1']
        discipline1 = self.disciplinemodel.getbykey(discipline1key)

        discipline2key = form.cleaneddata['discipline2']
        discipline2 = self.disciplinemodel.getbykey(discipline2key)

        disciplines = [discipline1, discipline2]

        character = self.model(name=form.cleaneddata['name'])
        character.description = form.cleaneddata['description']
        character.profession = profession
        character.race = race
        character.disciplines = disciplines

        # All of the following bits of logic require keys, so make
        # sure the keys exist before running them.
        if not self.user.key:
            self.user.put()

        character.owner = self.user
        character.put()

        self.user.characters.append(character)
        self.user.put()

        return character


class CharacterEdit(CharacterBase, Edit):

    def formcontext(self, item):
        formcontext = {
            'name': item.name,
            'profession': item.profession.key.urlsafe(),
            'race': item.race.key.urlsafe(),
            'discipline1': item.disciplines[0].key.urlsafe(),
            'discipline2': item.disciplines[1].key.urlsafe(),
            'description': item.description,
        }
        return formcontext

    def updateitem(self, item, form):
        item.name = form.cleaneddata['name']
        item.description = form.cleaneddata['description']

        professionkey = form.cleaneddata['profession']
        item.profession = self.professionmodel.getbykey(professionkey)

        racekey = form.cleaneddata['race']
        item.race = self.racemodel.getbykey(racekey)

        discipline1key = form.cleaneddata['discipline1']
        discipline2key = form.cleanedddata['discipline2']

        item.disciplines = [
            self.disciplinemodel.getbykey(discipline1key),
            self.disciplinemodel.getbykey(discipline2key),
        ]

        return item


class CharacterDelete(CharacterBase, Delete):

    def get(self, itemkey, *args, **kwargs):
        item = self.model.getbykey(itemkey)
        item.owner.characters.remove(item)
        item.owner.put()
        return super(CharacterDelete, self).get(itemkey, *args, **kwargs)


routes = [
    Route(r'/', CharacterHome, name='account-character-home'),
    Route(r'/create', CharacterCreate, name='account-character-create'),
    Route(r'/edit/<itemkey>', CharacterEdit,
          name='account-character-edit'),
    Route(r'/delete/<itemkey>', CharacterDelete,
          name='account-character-delete'),
]