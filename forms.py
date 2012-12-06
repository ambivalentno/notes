from django import forms

from notes.widgets import NewTextarea
from notes.models import Note


class NoteAdminForm(forms.ModelForm):
    '''Form to edit Note in admin'''
    text = forms.CharField(widget=NewTextarea())

    class Meta:
        model = Note


class NoteForm(forms.ModelForm):
    '''Form for Note object. Counts symbols'''
    def __init__(self, *args, **kwargs):
        data = kwargs.pop('data', None)
        files = kwargs.pop('files', None)
        super(NoteForm, self).__init__(data=data, files=files)
        self.fields['text'] = forms.CharField(widget=NewTextarea(),
         min_length=10)

    class Meta:
        model = Note
