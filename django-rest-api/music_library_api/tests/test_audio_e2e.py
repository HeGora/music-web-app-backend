from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from music_library_api.models import Audio, Playlist, Artist, AudioTag
from django.core.files.uploadedfile import SimpleUploadedFile


# TODO: refactor with data-factory library
class AudioViewSetTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.force_authenticate(user=self.user)
        self.artist = Artist.objects.create(name='Sample Artist', owner=self.user)
        self.tag = AudioTag.objects.create(name='Sample Tag')
        self.playlist = Playlist.objects.create(name='Sample Playlist', owner=self.user)   
        self.audio_file = SimpleUploadedFile("file.mp3", b"file_content", content_type="audio/mpeg")
        self.audio_data = {
            'name': 'Sample Audio',
            'album': [self.playlist.id],
            'artists': [{'name': self.artist.name}],
            'tags': [{'name': self.tag.name}],
            'owner': self.user.id,
            'audio_file': self.audio_file
        }

    def test_create_audio(self):
        url = reverse('audio-list')
        response = self.client.post(url, self.audio_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Audio.objects.count(), 1)
        audio = Audio.objects.get()
        self.assertEqual(audio.name, self.audio_data['name'])
        self.assertEqual(audio.album.id, self.playlist.id)
        self.assertEqual(list(audio.artists.values_list('name', flat=True)), [self.artist.name])
        self.assertEqual(list(audio.tags.values_list('name', flat=True)), [self.tag.name])
        self.assertTrue(audio.audio_file.name.endswith('file.mp3'))

    def test_retrieve_audio(self):
        audio = Audio.objects.create(name='Sample Audio', owner=self.user, audio_file=self.audio_file)
        audio.artists.add(self.artist)
        audio.tags.add(self.tag)
        url = reverse('audio-detail', args=[audio.id])  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Sample Audio')
        self.assertEqual(response.data['album']['id'], self.playlist.id)
        self.assertEqual(response.data['artists'][0]['name'], self.artist.name)
        self.assertEqual(response.data['tags'][0]['name'], self.tag.name)
        self.assertTrue(response.data['audio_file'].endswith('file.mp3'))

    def test_update_audio(self):
        audio = Audio.objects.create(name='Sample Audio', owner=self.user, audio_file=self.audio_file)
        audio.artists.add(self.artist)
        audio.tags.add(self.tag)
        new_artist = Artist.objects.create(name='Updated Artist', owner=self.user)
        new_tag = AudioTag.objects.create(name='Updated Tag')
        update_data = {
            'name': 'Updated Audio',
            'album': [self.playlist.id],
            'artists': [{'name': new_artist.name}],
            'tags': [{'name': new_tag.name}],
            'audio_file': self.audio_file
        }
        url = reverse('audio-detail', args=[audio.id])  
        response = self.client.put(url, update_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        audio.refresh_from_db()
        self.assertEqual(audio.name, 'Updated Audio')
        self.assertEqual(audio.album.id, self.playlist.id)
        self.assertEqual(list(audio.artists.values_list('name', flat=True)), [new_artist.name])
        self.assertEqual(list(audio.tags.values_list('name', flat=True)), [new_tag.name])
        self.assertTrue(audio.audio_file.name.endswith('file.mp3'))

    def test_delete_audio(self):
        audio = Audio.objects.create(name='Sample Audio', owner=self.user, audio_file=self.audio_file)
        url = reverse('audio-detail', args=[audio.id])  
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Audio.objects.count(), 0)

    def test_list_audio(self):
        Audio.objects.create(name='Audio 1', owner=self.user, audio_file=self.audio_file)
        Audio.objects.create(name='Audio 2', owner=self.user, audio_file=self.audio_file)
        url = reverse('audio-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)