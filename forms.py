from django import forms
from django.forms.widgets import HiddenInput
from widgets import MultiCount

class NewNoteForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(NewNoteForm, self).__init__()
        name = kwargs.pop('name')
        title_name = 'title'
        text_name = 'text' + name
        self.fields['form_name'] = forms.CharField(widget=HiddenInput(), initial=name)
        self.fields[title_name] = forms.CharField(max_length=50)
        self.fields[text_name] = forms.CharField(min_length=10, widget=MultiCount(name=name))
    
