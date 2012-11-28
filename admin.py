
from django.contrib import admin

from my_test.apps.notes.models import Note
from my_test.apps.notes.forms import NoteAdminForm


class NoteAdmin(admin.ModelAdmin):
    '''class to add a link from Note to the custom widget in form'''
    form = NoteAdminForm


admin.site.register(Note, NoteAdmin)
