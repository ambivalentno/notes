from django.forms.widgets import Textarea
from django.utils.safestring import mark_safe


class NewTextarea(Textarea):
    '''Textarea + symbol counter widget '''
    class Media:
        js = ('char_count_text_areas.js',)

    def render(self, name, value, attrs=None):
        try:
            attrs['class'] += ' countable'
        except KeyError:
            attrs['class'] = 'countable'

        base_html = super(NewTextarea, self).render(name, value,
         attrs=attrs)
        all_html = '<div>' + base_html + u'<p><span>0</span></p></div>'
        return mark_safe(all_html)
