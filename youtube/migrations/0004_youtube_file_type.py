# Generated by Django 4.1.7 on 2023-03-30 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("youtube", "0003_rename_audio_file_youtube_file_object"),
    ]

    operations = [
        migrations.AddField(
            model_name="youtube",
            name="file_type",
            field=models.CharField(default="audio", max_length=10),
            preserve_default=False,
        ),
    ]
