from django import forms
from django.forms.widgets import HiddenInput
from widgets import NewTextarea
from models import Note


class NoteAdminForm(forms.ModelForm):
    text = forms.CharField(widget=NewTextarea())

    class Meta:
        model = Note


class NoteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        formname = kwargs.pop('formname', 'add_form')
        data = kwargs.pop('data', None)
        files = kwargs.pop('files', None)
        super(NoteForm, self).__init__(data=data, files=files)
        newtextarea_attrs = {'id': formname}
        self.fields['text'] = forms.CharField(widget=NewTextarea(
            attrs=newtextarea_attrs), min_length=10)

    class Meta:
        model = Note
