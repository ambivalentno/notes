from django import template

register = template.Library()

@register.inclusion_tag('show_note.html')
def show_note(note):
    return {'title': note.title, 'text': note.text}
