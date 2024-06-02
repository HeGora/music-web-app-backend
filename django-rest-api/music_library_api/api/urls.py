from django.urls import path, include
from rest_framework import routers
from music_library_api.api.views import AudioViewSet, PlaylistViewSet, ArtistViewSet

router = routers.SimpleRouter()
router.register(r'audios', AudioViewSet, basename='audio')
router.register(r'playlists', PlaylistViewSet, basename='playlist')
router.register(r'artists', ArtistViewSet, basename='artist')

urlpatterns = [
    path('', include(router.urls)),
]