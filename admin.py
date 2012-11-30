
from django.contrib import admin

from notes.models import Note
from notes.forms import NoteAdminForm


class NoteAdmin(admin.ModelAdmin):
    '''Class to add a link from Note to the custom widget in form'''
    form = NoteAdminForm


admin.site.register(Note, NoteAdmin)
