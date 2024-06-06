from django.contrib.auth.models import User
from django.test import TestCase
from music_library_api.models import Audio, Artist, AudioTag
from music_library_api.api.serializers import AudioSerializer

# TODO: refactor using data-factory library
class AudioSerializerTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.artist = Artist.objects.create(name='Sample Artist', owner=self.user)
        self.tag = AudioTag.objects.create(name='Sample Tag')
        self.audio_data = {
            'name': 'Sample Audio',
            'album': None,
            'artists': [{'name': self.artist.name}],
            'tags': [{'name': self.tag.name}],
            'owner': self.user.id
        }

    def test_create_audio(self):
        serializer = AudioSerializer()
        audio = serializer.create(self.audio_data)
        self.assertEqual(audio.name, 'Sample Audio')
    
    def test_update_audio(self):
        audio = Audio.objects.create(name='Old Audio', owner=self.user)
        serializer = AudioSerializer(instance=audio)
        updated_audio_data = {
            'name': 'Updated Audio',
            'album': None,  
            'artists': [{'name': self.artist.name}],
            'tags': [{'name': self.tag.name}],
            'owner': self.user.id
        }
        audio = serializer.update(audio, updated_audio_data)
        self.assertEqual(audio.name, 'Updated Audio')

    def test_to_internal_value_audio(self):
        serializer = AudioSerializer()
        internal_data = serializer.to_internal_value(self.audio_data)
        self.assertEqual(internal_data['name'], 'Sample Audio')

    def test_get_or_create_nested_fields_audio(self):
        serializer = AudioSerializer()
        nested_data = [{'name': self.artist.name}]
        nested_objects = serializer.get_or_create_nested_objects(nested_data, Artist)
        self.assertEqual(nested_objects[0].name, self.artist.name)