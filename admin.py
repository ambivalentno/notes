from django.contrib import admin
from notes.models import Note
from forms import NoteAdminForm


class NoteAdmin(admin.ModelAdmin):
    form = NoteAdminForm


admin.site.register(Note, NoteAdmin)
