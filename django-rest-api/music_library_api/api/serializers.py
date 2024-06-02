from rest_framework import serializers
from music_library_api.models import Audio, Playlist, Artist, AudioTag

class AlbumShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['id', 'name']
    
class PlaylistNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        ##other fields would be added later(duration, image, etc)
        fields = ['id', 'name']

class ArtistSerializer(serializers.ModelSerializer):
    albums = PlaylistNestedSerializer(many=True, required=False)

    def create(self, validated_data):
        albums = validated_data.pop('albums', [])
        playlist = Artist.objects.create(**validated_data)
        playlist.albums.set(albums)
        return playlist

    def update(self, instance, validated_data):
        albums = validated_data.pop('albums', None)
        if albums is not None:
            instance.albums.set(albums)
        fields = ['name']
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except KeyError:  
                pass
        instance.save()
        return instance

    def to_internal_value(self, data):
        albums_data = data.pop('albums', None)
        validated_data = super().to_internal_value(data)
        if albums_data is not None:
            validated_data['albums'] = Playlist.objects.filter(id__in=albums_data)
        return validated_data

    class Meta:
        model = Artist
        fields = ['id', 'name', 'albums']

class ArtistNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name']

class AudioTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioTag
        fields = ['id', 'name']

class AudioSerializer(serializers.ModelSerializer):
    album = AlbumShortSerializer(required=False)
    artists = ArtistNestedSerializer(many=True, required=False)
    tags = AudioTagSerializer(many=True, required=False)

    def create(self, validated_data):
        artists = validated_data.pop('artists', [])
        tags = validated_data.pop('tags', [])
        audio = Audio.objects.create(**validated_data)
        audio.artists.set(artists)
        audio.tags.set(tags)
        return audio

    def update(self, instance, validated_data):
        artists = validated_data.pop('artists', None)
        tags = validated_data.pop('tags', None)
        if artists is not None:
            instance.artists.set(artists)
        if tags is not None:
            instance.tags.set(tags)
        fields = ['name', 'album']
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except KeyError:  
                pass
        instance.save()
        return instance
    
    def get_or_create_nested_objects(self, nested_data, nested_class):
        nested_fields = []
        for instance_data in nested_data:
            instance, created = nested_class.objects.get_or_create(**instance_data)
            nested_fields.append(instance)
        return nested_fields

    
    def to_internal_value(self, data):
        artists_data = data.pop('artists', None)
        tags_data = data.pop('tags', None)
        album_data = data.pop('album', None)
        validated_data = super().to_internal_value(data)
        if album_data is not None:
            if album_data[0]:
                validated_data['album'] = Playlist.objects.get(**album_data[0])
            else:
                validated_data['album'] = None
        if artists_data is not None:
            validated_data['artists'] = self.get_or_create_nested_objects(artists_data[0], Artist)
        if tags_data is not None:
            validated_data['tags'] = self.get_or_create_nested_objects(tags_data[0], AudioTag)
        return validated_data

    class Meta:
        model = Audio
        fields = ['id', 'audio_file', 'name', 'album', 'tags', 'artists']

class PlaylistSerializer(serializers.ModelSerializer):
    audios = AudioSerializer(many=True, required=False)
    album_artists = ArtistNestedSerializer(many=True, required=False)

    def create(self, validated_data):
        audios = validated_data.pop('audios', [])
        album_artists = validated_data.pop('album_artists', [])
        playlist = Playlist.objects.create(**validated_data)
        playlist.audios.set(audios)
        playlist.album_artists.set(album_artists)
        return playlist

    def update(self, instance, validated_data):
        audios = validated_data.pop('audios', None)
        album_artists = validated_data.pop('album_artists', None)
        if audios is not None:
            instance.audios.set(audios)
        if album_artists is not None:
            instance.album_artists.set(album_artists)
        fields = ['name']
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except KeyError:  
                pass
        instance.save()
        return instance

    def to_internal_value(self, data):
        audios_data = data.pop('audios', None)
        artists_data = data.pop('album_artists', None)
        validated_data = super().to_internal_value(data)
        if audios_data is not None:
            validated_data['audios'] = Audio.objects.filter(id__in=audios_data)
        if artists_data is not None:
            validated_data['album_artists'] = Artist.objects.filter(id__in=artists_data)
        return validated_data

    class Meta:
        model = Playlist
        fields = ['id', 'name', 'audios', 'album_artists']