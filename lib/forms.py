from django import forms
from django.utils.safestring import mark_safe


class Base(forms.Form):
    validate = False

    @property
    def isvalid(self):
        return self.is_valid()

    @property
    def cleaneddata(self):
        return self.cleaned_data

    def makeelements(self, boundfield):
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
            stringparts.append(unicode(boundfield))

        stringparts.append(unicode(label))

        if isinstance(field.widget, forms.Textarea):
            stringparts.append('<br/>')

        if not isinstance(field.widget, forms.CheckboxInput):
            stringparts.append(unicode(boundfield))

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