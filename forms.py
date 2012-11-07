from django import forms
from django.forms.widgets import HiddenInput
from widgets import MultiCount, NewTextarea

class NewNoteForm(forms.Form):

    def __init__(self, data=None):
        super(NewNoteForm, self).__init__(data=data)
        name = data['form_name']
        self.fields['form_name'] = forms.CharField(widget=HiddenInput(), initial=name)
        self.fields['title'] = forms.CharField(max_length=50)
        self.fields['text'] = forms.MultiValueField(
            fields=[forms.CharField(min_length=10), forms.CharField()],
            widget=MultiCount(name=name))

    def clean_text(self):
        print self.cleaned_data
        data = self.cleaned_data['text']
        if len(data[0]) < 10:
            raise forms.ValidationError("You need to post smth longer than 10 symbols.")
        return data


