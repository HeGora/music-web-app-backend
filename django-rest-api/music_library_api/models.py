from django.db import models

class Audio(models.Model):
    name = models.CharField(max_length = 200)
    duration = models.DurationField()
    #album

class Playlist:
    name = models.CharField(max_length = 200)

class AudioTag:
    name = models.CharField(max_length = 100)

class Artist:
    name = models.CharField(max_length = 200)