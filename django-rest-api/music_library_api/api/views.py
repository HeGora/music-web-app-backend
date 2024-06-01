from music_library_api.models import Audio
from music_library_api.api.serializers import AudioSerializer
from rest_framework import viewsets
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from common.parsers import MultipartJSONParser

class AudioViewSet(viewsets.ModelViewSet):

    queryset = Audio.objects.all()
    serializer_class = AudioSerializer
    parser_classes = [MultipartJSONParser, JSONParser]