from django.forms.widgets import TextInput, Textarea, MultiWidget
from django.utils.safestring import mark_safe
from django.forms.util import flatatt
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode
from django import forms

class MultiCount(MultiWidget):
    class Media:
        js = ('test.js',)

    def __init__(self, name=None, text_area_attrs={}, input_attrs={'disabled':'disabled'}):
        input_name = "id_text" + name +"_0"
        output_name = "id_text" + name +"_1"
        text_area_attrs['onclick'] = "somef('"+input_name+"','"+output_name+"')"
        self.widgets = (Textarea(attrs=text_area_attrs), TextInput(attrs=input_attrs))   
        super(MultiCount,self).__init__(self.widgets)

    def decompress(self, values):
        if values:
            return values
        return [None, None]



