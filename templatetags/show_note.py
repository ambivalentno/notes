from django import template
from my_test.apps.notes.models import Note

register = template.Library()


@register.inclusion_tag('show_note.html')
def show_note(note_id):
    note = Note.objects.get(id=note_id)
    return {'title': note.title, 'text': note.text, 'image': note.image}
