from my_test.apps.notes.models import Note


def default(request):
    '''Returns number of all Note objecs as notes_number'''

    all_notes = Note.objects.all().count()
    return {'notes_number': all_notes}
