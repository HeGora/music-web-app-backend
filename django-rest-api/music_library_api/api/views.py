from music_library_api.models import Audio, Playlist, Artist
from music_library_api.api.serializers import AudioSerializer, PlaylistSerializer
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from common.parsers import MultipartJSONParser
from common.permissions import IsOwner

class AudioViewSet(viewsets.ModelViewSet):

    queryset = Audio.objects.all()
    serializer_class = AudioSerializer
    parser_classes = [MultipartJSONParser, JSONParser]
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Audio.objects.filter(owner=self.request.user)

class PlaylistViewSet(viewsets.ModelViewSet):

    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Playlist.objects.filter(owner=self.request.user)