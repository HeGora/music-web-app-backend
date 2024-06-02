from django.contrib import admin
from music_library_api.models import Audio, Playlist, Artist, AudioTag, PlaylistAudio

# Register your models here.
admin.site.register(Audio)
admin.site.register(Playlist)
admin.site.register(Artist)
admin.site.register(AudioTag)
admin.site.register(PlaylistAudio)
