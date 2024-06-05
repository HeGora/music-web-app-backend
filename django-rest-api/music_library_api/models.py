from django.db import models
from django.contrib.auth.models import User

class Audio(models.Model):
    audio_file = models.FileField(upload_to='audios/', null=True, blank=True)
    name = models.CharField(max_length = 200)
    duration = models.DurationField(null=True, blank=True)
    owner = models.ForeignKey(
        User, 
        related_name='audios', 
        on_delete=models.CASCADE, 
        null=True
        )
    album = models.ForeignKey(
        'Playlist', 
        blank=True, 
        null=True, 
        on_delete=models.SET_NULL,
        )
    artists = models.ManyToManyField(
        'Artist',
        related_name='audios', 
        blank=True,
        )
    tags = models.ManyToManyField(
        'AudioTag',
        related_name='audios', 
        blank=True,
        )
    
class Playlist(models.Model):
    name = models.CharField(max_length = 200)
    owner = models.ForeignKey(
        User, 
        related_name='playlists', 
        on_delete=models.CASCADE, 
        null=True
        )
    audios = models.ManyToManyField(
        Audio,
        through='PlaylistAudio',
        through_fields=('playlist', 'audio'),
        blank=True,
        )

class PlaylistAudio(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    audio = models.ForeignKey(Audio, on_delete=models.CASCADE)
    ##order_number = models.PositiveSmallIntegerField(unique=True)

class Artist(models.Model):
    name = models.CharField(max_length = 200, unique=True)
    owner = models.ForeignKey(
        User, 
        related_name='artists',
        on_delete=models.CASCADE,
        null= True
        )
    albums = models.ManyToManyField(
        Playlist, 
        related_name='album_artists',
        blank=True
        )


class AudioTag(models.Model):
    name = models.CharField(max_length = 100, unique=True)