from django.forms.widgets import Textarea
from django.utils.safestring import mark_safe
from django.forms.util import flatatt


class NewTextarea(Textarea):
    class Media:
        js = ('test.js',)

    def __init__(self, attrs=None):
        default_attrs = {'name': 'default_name', 'id': 'default_id'}
        if attrs:
            default_attrs.update(attrs)

        default_attrs['onclick'] = "somef('" + default_attrs['id'] + \
            "','output_" + default_attrs['id'] + "')"
        super(NewTextarea, self).__init__(attrs=default_attrs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name='text')
        base_html = super(NewTextarea, self).render(name, value,
         attrs=final_attrs)
        output_id = u' id=output_' + final_attrs['id']
        counter = u'<p%s></p>' % output_id
        all_html = base_html + counter
        return mark_safe(all_html)
