from django import forms
from django.forms.widgets import HiddenInput
from widgets import NewTextarea


class NewNoteForm(forms.Form):

    def __init__(self, attrs=None, formname='add_note'):
        super(NewNoteForm, self).__init__(data=attrs)
        name = formname
        self.fields['form_name'] = forms.CharField(widget=HiddenInput(),
         initial=name)
        self.fields['title'] = forms.CharField(max_length=50)
        newtextarea_attrs = {'id': name}
        self.fields['text'] = forms.CharField(widget=NewTextarea(
            attrs=newtextarea_attrs),
            min_length=10)
