from my_test.apps.notes.models import Note


def default(request):
    '''Returns number of all Note objecs as NOTES_NUMBER'''

    all_notes = Note.objects.all().count()
    return {'NOTES_NUMBER': all_notes}
