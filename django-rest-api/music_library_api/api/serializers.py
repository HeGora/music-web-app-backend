from rest_framework import serializers
from music_library_api.models import Audio, Playlist, Artist, AudioTag

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fileds = ['id', 'name']

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name']

class AudioTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioTag
        fields = ['id', 'name']

class AudioSerializer(serializers.ModelSerializer):
    album = AlbumSerializer(required=False)
    artists = ArtistSerializer(many=True, required=False, read_only=False)
    tags = AudioTagSerializer(many=True, required=False)
    
    def update_or_create_relations(self, relations, relation_class):
        relations_ids = []
        for relation in relations:
            relation_instance, created = relation_class.objects.update_or_create(**relation)
            relations_ids.append(relation_instance.pk)
        return relations_ids

    def create(self, validated_data):
        artists = validated_data.pop('artists', [])
        tags = validated_data.pop('tags', [])
        audio = Audio.objects.create(**validated_data)
        audio.artists.set(artists)
        audio.tags.set(tags)
        return audio

    def update(self, instance, validated_data):
        artists = validated_data.pop('artists', [])
        tags = validated_data.pop('tags', [])
        instance.artists.set(self.update_or_create_relations(artists, Artist))
        instance.tags.set(self.update_or_create_relations(tags, AudioTag))
        fields = ['name', 'album']
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except KeyError:  
                pass
        instance.save()
        return instance
    
    def get_or_create_nested_fields(self, nested_data, nested_class):
        nested_fields = []
        for instance_data in nested_data:
            instance, created = nested_class.objects.get_or_create(**instance_data)
            nested_fields.append(instance)
        return nested_fields

    
    def to_internal_value(self, data):
        artists_data = data.pop('artists', [])
        tags_data = data.pop('tags', [])
        validated_data = super().to_internal_value(data)
        validated_data['artists'] = self.get_or_create_nested_fields(artists_data[0], Artist)
        validated_data['tags'] = self.get_or_create_nested_fields(tags_data[0], AudioTag)
        return validated_data

    class Meta:
        model = Audio
        fields = ['id', 'audio_file', 'name', 'album', 'tags', 'artists']

class PlaylistReadSerializer(serializers.ModelSerializer):
    audios = AudioSerializer(many=True)
    artists = ArtistSerializer(many=True)

    class Meta:
        model = Playlist
        fields = ['id', 'name', 'audios', 'artists']

class PlaylistWriteSerializer(serializers.ModelSerializer):
    artists = ArtistSerializer(many=True)

    class Meta:
        model = Playlist
        fields = ['id', 'name', 'artist']