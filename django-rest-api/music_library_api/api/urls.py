from django.urls import path, include
from rest_framework import routers
from music_library_api.api.views import AudioViewSet, PlaylistViewSet

router = routers.SimpleRouter()
router.register(r'audios', AudioViewSet, basename='audio')
router.register(r'playlists', PlaylistViewSet, basename='playlist')

urlpatterns = [
    path('', include(router.urls)),
]