from django.contrib.auth.models import User
from django.test import TestCase
from music_library_api.models import Audio, Playlist, Artist
from music_library_api.api.serializers import PlaylistSerializer

# TODO: refactor using data-factory library
class PlaylistSerializerMethodTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.audio = Audio.objects.create(name='Sample Audio', owner=self.user)
        self.artist = Artist.objects.create(name='Sample Artist', owner=self.user)
        self.playlist_data = {
            'name': 'Sample Playlist',
            'audios': [self.audio.id],
            'album_artists': [self.artist.id],
            'owner': self.user.id
        }

    def test_create_playlist(self):
        serializer = PlaylistSerializer()
        playlist = serializer.create(self.playlist_data)
        self.assertEqual(playlist.name, 'Sample Playlist')
    
    def test_update_playlist(self):
        playlist = Playlist.objects.create(name='Old Playlist', owner=self.user)
        serializer = PlaylistSerializer(instance=playlist)
        updated_playlist_data = {
            'name': 'Updated Playlist',
            'audios': [self.audio.id],
            'album_artists': [self.artist.id],
            'owner': self.user.id
        }
        playlist = serializer.update(playlist, updated_playlist_data)
        self.assertEqual(playlist.name, 'Updated Playlist')

    def test_to_internal_value_playlist(self):
        serializer = PlaylistSerializer()
        internal_data = serializer.to_internal_value(self.playlist_data)
        self.assertEqual(internal_data['name'], 'Sample Playlist')

    def test_get_or_create_nested_fields_playlist(self):
        serializer = PlaylistSerializer()
        nested_data = [{'name': self.artist.name}]
        nested_objects = serializer.get_or_create_nested_objects(nested_data, Artist)
        self.assertEqual(nested_objects[0].name, self.artist.name)