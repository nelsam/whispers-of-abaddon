import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from copy import deepcopy

from django import forms
#from django.utils.safestring import mark_safe

from models.character import (Profession as ProfessionModel,
                              Race as RaceModel,
                              Discipline as DisciplineModel)
from models.account import Rank as RankModel


class Base(forms.Form):
    """
    The base form - much base functionality is here, most
    forms should extend this.
    """
    validate = False

    @property
    def isvalid(self):
        """
        I'm trying to keep the use of the shift key down.
        This is just an alias for self.is_valid() for the
        sake of consistency.
        """
        return self.is_valid()

    @property
    def cleaneddata(self):
        """
        I'm trying to keep the use of the shift key down.
        This is just an alias for self.cleaned_data for the
        sake of consistency.
        """
        return self.cleaned_data

    def makeelements(self, boundfield):
        """
        Creates all HTML elements for a given boundfield.

        :returns: The raw HTML code for the passed in element.
        """
        field = boundfield.field

        stringparts = []

        label = boundfield.label_tag()
        if field.required:
            label = label.replace('>', '><span class="required">*</span>', 1)

        if self.validate and boundfield.name in self.errors:
            messages = self.errors[boundfield.name]

            labelEndIndex = label.find('</label>')
            labelStart = label[:labelEndIndex]
            labelEnd = label[labelEndIndex:]

            labelParts = [labelStart]
            for message in messages:
                labelParts.append('<span class="message">%s</span>' % message)
            labelParts.append(labelEnd)
            label = ''.join(labelParts)

        stringparts.append('<div>')

        if isinstance(field.widget, forms.CheckboxInput):
            stringparts.append(str(boundfield))

        stringparts.append(str(label))

        if isinstance(field.widget, forms.Textarea):
            stringparts.append('<br/>')

        if not isinstance(field.widget, forms.CheckboxInput):
            stringparts.append(str(boundfield))

        stringparts.append('</div>')

        return '\n'.join(stringparts)

    def __unicode__(self):
        stringparts = ['<div>']
        for field in self:
            stringparts.append(self.makeelements(field))
        stringparts.append('</div>')
        return '\n'.join(stringparts)

    def __str__(self):
        return self.__unicode__()


class TwoColumn(Base):
    fieldsbeforecolumns = None
    columnedfields = None

    def __unicode__(self):

        stringparts = ['<div>']

        for fieldname in self.fieldsbeforecolumns:
            field = self[fieldname]
            stringparts.append(self.makeelements(field))

        twocolumnparts = []
        leftcolumn = True
        for fieldname in self.columnedfields:
            field = self[fieldname]
            if leftcolumn:
                twocolumnparts.append('<div class="two-column-form">')

            twocolumnparts.append(self.makeelements(field))

            if not leftcolumn:
                twocolumnparts.append('</div>')

            leftcolumn = not leftcolumn

        if not leftcolumn:
            twocolumnparts.append('</div>')

        stringparts.extend(twocolumnparts)

        for fieldname in self.fields:
            if (fieldname not in self.fieldsbeforecolumns and
                fieldname not in self.columnedfields):
                field = self[fieldname]
                stringparts.append(self.makeelements(field))

        stringparts.append('</div>')

        return '\n'.join(stringparts)


class Record(Base):
    """
    This is intended to help with storing any Record data type.
    Remember that an Record must use a "section" to tell it
    which part of the website it belongs in - this form does not
    do that part for you.  It just loads the user input data - namely,
    the title and body.
    """
    title = forms.CharField(label="Title: ")
    body = forms.CharField(label="Body: ", widget=forms.Textarea())


class OrderedRecord(Record):
    """
    Handles any records that have a rank.
    """
    rank = forms.IntegerField(label="Order Rank")


class Rank(Record):
    """
    This form handles rank data for the guild.  It's mainly just
    an ordered record, but in a separate collection so that we can
    do more with it when the site calls for restricted areas.
    """
    placement = forms.IntegerField(label="Hierarchy Placement")


class Account(Base):
    """
    The main account form.  Some aspects of the account will need
    to be handled on separate pages, but this will handle the base
    stuff.
    """
    name = forms.CharField(label="Display Name: ")
    about = forms.CharField(label="About You: ", widget=forms.Textarea())


baseranks = [('', 'Not a Member')]
allranks = deepcopy(baseranks)
allranks.extend([(rank.key.urlsafe(), rank.name)
                 for rank in RankModel.hierarchy()])


class AdminAccount(Account):
    """
    Same as an account, but allows admins to set a few other things.
    """
    isadmin = forms.BooleanField(label="Site Admin", required=False)
    rank = forms.ChoiceField(choices=allranks,
                             widget=forms.Select(),
                             label="Guild Rank",
                             required=False)

    def __init__(self, *args, **kwargs):
        if 'maxrank' in kwargs:
            maxrank = kwargs['maxrank']
            del kwargs['maxrank']
            ranks = deepcopy(baseranks)
            ranks.extend([(rank.key.urlsafe(), rank.name)
                          for rank in RankModel.hierarchy(maxrank=maxrank)])

        super(AdminAccount, self).__init__(*args, **kwargs)

        self.fields['rank'].choices = ranks


professions = [(profession.key.urlsafe(), profession.name)
               for profession in ProfessionModel.query()]
races = [(race.key.urlsafe(), race.name)
         for race in RaceModel.query()]
disciplines = [(discipline.key.urlsafe(), discipline.name)
               for discipline in DisciplineModel.query()]


class Character(Base):
    """
    A form to allow a user to attach a character to their account.
    """
    name = forms.CharField(label="Name: ")
    profession = forms.ChoiceField(choices=professions,
                                   widget=forms.Select(),
                                   label="Profession: ")
    race = forms.ChoiceField(choices=races,
                             widget=forms.Select(),
                             label="Race: ")
    discipline1 = forms.ChoiceField(choices=disciplines,
                                    widget=forms.Select(),
                                    label="First Crafting Discipline: ")
    discipline2 = forms.ChoiceField(choices=disciplines,
                                    widget=forms.Select(),
                                    label="Second Crafting Discipline: ")
    description = forms.CharField(label="Character Profile: ",
                                  widget=forms.Textarea())


class Message(Base):
    """
    Form to send a message to another user.
    """
    subject = forms.CharField(label="Subject: ")
    message = forms.CharField(label="Message: ", widget=forms.Textarea())


class Reply(Base):
    """
    Form to reply to another user.
    """
    message = forms.CharField(label="Message: ", widget=forms.Textarea())


class Forum(Record):
    """
    Form to create a forum
    """
    viewlevel = forms.IntegerField(label="View Level: ")
    replylevel = forms.IntegerField(label="Reply Level: ")
    newthreadlevel = forms.IntegerField(label="New Thread Level: ")
