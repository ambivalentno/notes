from django.forms.widgets import Textarea
from django.utils.safestring import mark_safe


class NewTextarea(Textarea):
    '''Textarea + symbol counter widget '''
    class Media:
        js = ('adding.js',)

    def __init__(self, attrs=None):
        default_attrs = {'name': 'default_name', 'id': 'default_id'}
        if attrs:
            default_attrs.update(attrs)
        super(NewTextarea, self).__init__(attrs=default_attrs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name='text')
        base_html = super(NewTextarea, self).render(name, value,
         attrs=final_attrs)
        output_id = u' id=output_' + final_attrs['id']
        script = u'<script> django.jQuery(document).ready(function(){ \
            django.jQuery("#%s").charCount();}); </script>' % final_attrs['id']
        all_html = base_html + script
        return mark_safe(all_html)
