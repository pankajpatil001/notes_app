from django.urls import path
from notes import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('notes/create/', views.create_notes, name='create_notes'),
    path('notes/share/', views.share_note, name='share_note'),
    path('notes/version-history/<str:id>/', views.note_version_history, name='note_version_history'),
    path('notes/<str:id>/', views.NoteRetriveUpdate.as_view(), name='note'),
]