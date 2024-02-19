from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from notes.models import *

class NoteAPITests(APITestCase):
    def setUp(self):
        self.user = NeofiUser.objects.create_user(email='email@test.com', username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)

    def test_note_create(self):
        url = reverse('create_notes')
        data = {'content': 'This is a test note.'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 1)

    def test_note_retrieve(self):
        note = Note.objects.create(owner=self.user, content='This is a test note.')
        NoteShare.objects.create(note=note, user=self.user)
        url = reverse('note', kwargs={'id': note.id})
        response = self.client.get(url)
        print('response', response.status_code, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_note_share(self):
        note = Note.objects.create(owner=self.user, content='This is a test note.')
        user2 = NeofiUser.objects.create_user(email='email2@test.com', username='testuser2', password='password123')
        url = reverse('share_note')
        data = {'note_id': note.id, 'user_ids': [user2.id]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(NoteShare.objects.filter(note=note, user=user2).exists())

    def test_note_update(self):
        note = Note.objects.create(owner=self.user, content='This is a test note.')
        NoteShare.objects.create(note=note, user=self.user)
        url = reverse('note', kwargs={'id': note.id})
        data = {'content': 'This is a test note. With added content.'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        note.refresh_from_db()
        self.assertEqual(note.content, 'This is a test note. With added content.')

    def test_note_version_history(self):
        note = Note.objects.create(owner=self.user, content='This is a test note.')
        note_share = NoteShare.objects.create(note=note, user=self.user)
        NoteEdit.objects.create(note=note, edited_by=self.user, previous_content='', edited_content='new content')
        url = reverse('note_version_history', kwargs={'id': note.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class UserAPITests(APITestCase):
    def test_user_signup(self):
        url = reverse('signup')
        data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'password123', 'confirm_password': 'password123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        user = NeofiUser.objects.create_user(email='email@test.com', username='testuser', password='password123')
        url = reverse('login')
        data = {'email': 'email@test.com', 'password': 'password123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)