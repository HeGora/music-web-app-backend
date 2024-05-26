from django.db import models

class Audio(models.Model):
    audio_file = models.FileField('audios/')
    name = models.CharField(max_length = 200)
    duration = models.DurationField()
    album = models.ForeignKey(
        'Playlist', 
        blank=True, 
        null=True, 
        on_delete=models.SET_NULL,
        )
    artists = models.ManyToManyField('Artist', related_name='audios')
    tags = models.ManyToManyField('AudioTag', related_name='audios')
    
class Playlist(models.Model):
    name = models.CharField(max_length = 200)
    audios = models.ManyToManyField(
        Audio,
        through='PlaylistAudio',
        through_fields=('playlist', 'audio'),
        )
    artists = models.ManyToManyField('Artist')

class PlaylistAudio(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    audio = models.ForeignKey(Audio, on_delete=models.CASCADE)
    ##order_number = models.PositiveSmallIntegerField(unique=True)

class Artist(models.Model):
    name = models.CharField(max_length = 200)


class AudioTag(models.Model):
    name = models.CharField(max_length = 100)