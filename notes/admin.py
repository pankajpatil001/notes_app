from django.contrib import admin
from notes.models import NeofiUser, Note, NoteEdit, NoteShare

admin.site.register(NeofiUser)
admin.site.register(Note)
admin.site.register(NoteEdit)
admin.site.register(NoteShare)
