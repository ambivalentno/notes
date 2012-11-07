from django.forms.widgets import TextInput, Textarea, MultiWidget, Widget
from django.utils.safestring import mark_safe
from django.forms.util import flatatt
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode
from django import forms

class NewTextarea(Widget):
    class Media:
        js = ('test.js',)

    def __init__(self, attrs=None):
        # The 'rows' and 'cols' attributes are required for HTML correctness.
        default_attrs = {'cols': '40', 'rows': '10'}
        if attrs:
            default_attrs.update(attrs)
        super(NewTextarea, self).__init__(default_attrs)

    def render(self, name, value, attrs=None):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name='text')
        first_html = u'<textarea%s>%s</textarea>' % (flatatt(final_attrs),
            conditional_escape(force_unicode(value)))
        return mark_safe(first_html)



class MultiCount(MultiWidget):
    class Media:
        js = ('test.js',)

    def __init__(self, name=None, text_area_attrs={}, input_attrs={'disabled':'disabled'}):
        input_id = "id_text" + name +"_0"
        output_id = "id_text" + name +"_1"
        text_area_attrs['onclick'] = "somef('"+input_id+"','"+output_id+"')"
        text_area_attrs['name'] = 'text'
        self.widgets = (NewTextarea(attrs=text_area_attrs), TextInput(attrs=input_attrs))   
        super(MultiCount,self).__init__(self.widgets)
        self.attrs['id'] = "id_text" + name

    def decompress(self, values):
        if values:
            return values
        return [None, None]
