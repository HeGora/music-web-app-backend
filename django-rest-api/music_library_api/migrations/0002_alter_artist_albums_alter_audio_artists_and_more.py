# Generated by Django 4.2.3 on 2024-05-27 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music_library_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='albums',
            field=models.ManyToManyField(blank=True, related_name='album_artists', to='music_library_api.playlist'),
        ),
        migrations.AlterField(
            model_name='audio',
            name='artists',
            field=models.ManyToManyField(blank=True, related_name='audios', to='music_library_api.artist'),
        ),
        migrations.AlterField(
            model_name='audio',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='audios', to='music_library_api.audiotag'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='audios',
            field=models.ManyToManyField(blank=True, through='music_library_api.PlaylistAudio', to='music_library_api.audio'),
        ),
    ]