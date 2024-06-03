from music_library_api.models import Audio, Playlist, Artist
from music_library_api.api.serializers import AudioSerializer, PlaylistSerializer, ArtistSerializer
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from common.parsers import MultipartJSONParser

class AudioViewSet(viewsets.ModelViewSet):

    queryset = Audio.objects.all()
    serializer_class = AudioSerializer
    parser_classes = [MultipartJSONParser, JSONParser]
    permission_classes = [IsAuthenticated]

class PlaylistViewSet(viewsets.ModelViewSet):

    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]

class ArtistViewSet(viewsets.ModelViewSet):

    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]