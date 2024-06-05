# Generated by Django 4.2.3 on 2024-06-04 13:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('music_library_api', '0005_alter_audio_audio_file_alter_audiotag_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='artists', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='audio',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='audios', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='playlist',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='playlists', to=settings.AUTH_USER_MODEL),
        ),
    ]
