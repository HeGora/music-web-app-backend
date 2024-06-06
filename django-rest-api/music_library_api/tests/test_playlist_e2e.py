from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from music_library_api.models import Playlist, Artist, Audio


#refactor using data-factory library
class PlaylistViewSetTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.force_authenticate(user=self.user)  
        self.audio = Audio.objects.create(name='Sample Audio', owner=self.user)
        self.artist = Artist.objects.create(name='Sample Artist', owner=self.user)
        self.playlist_data = {
            'name': 'Sample Playlist',
            'audios': [self.audio.id],
            'album_artists': [self.artist.id],
            'owner': self.user.id
        }

    def test_create_playlist(self):
        url = reverse('playlist-list')
        response = self.client.post(url, self.playlist_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Playlist.objects.count(), 1)
        playlist = Playlist.objects.get()
        self.assertEqual(playlist.name, 'Sample Playlist')
        self.assertEqual(list(playlist.audios.values_list('id', flat=True)), [self.audio.id])
        self.assertEqual(list(playlist.album_artists.values_list('id', flat=True)), [self.artist.id])
        self.assertEqual(playlist.owner, self.user)

    def test_retrieve_playlist(self):
        playlist = Playlist.objects.create(name='Sample Playlist', owner=self.user)
        playlist.audios.add(self.audio)
        playlist.album_artists.add(self.artist)
        url = reverse('playlist-detail', args=[playlist.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Sample Playlist')
        self.assertEqual(response.data['audios'][0], self.audio.id)
        self.assertEqual(response.data['album_artists'][0], self.artist.id)
        self.assertEqual(response.data['owner'], self.user.id)

    def test_update_playlist(self):
        playlist = Playlist.objects.create(name='Sample Playlist', owner=self.user)
        url = reverse('playlist-detail', args=[playlist.id])
        new_name = 'Updated Playlist'
        new_audio = Audio.objects.create(name='New Audio', owner=self.user)
        new_artist = Artist.objects.create(name='New Artist', owner=self.user)
        updated_data = {
            'name': new_name,
            'audios': [new_audio.id],
            'album_artists': [new_artist.id]
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        playlist.refresh_from_db()
        self.assertEqual(playlist.name, new_name)
        self.assertEqual(list(playlist.audios.values_list('id', flat=True)), [new_audio.id])
        self.assertEqual(list(playlist.album_artists.values_list('id', flat=True)), [new_artist.id])

    def test_delete_playlist(self):
        playlist = Playlist.objects.create(name='Sample Playlist', owner=self.user)
        url = reverse('playlist-detail', args=[playlist.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Playlist.objects.count(), 0)

    def test_list_playlists(self):
        Playlist.objects.create(name='Playlist 1', owner=self.user)
        Playlist.objects.create(name='Playlist 2', owner=self.user)
        url = reverse('playlist-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)