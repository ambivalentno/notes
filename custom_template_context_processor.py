from django.conf import settings
from models import Note


def default(request):
    all_notes = Note.objects.all()
    return {'NOTES_NUMBER': len(all_notes)}
