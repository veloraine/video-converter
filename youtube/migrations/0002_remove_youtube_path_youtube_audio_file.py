# Generated by Django 4.1.7 on 2023-03-30 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("youtube", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(model_name="youtube", name="path",),
        migrations.AddField(
            model_name="youtube",
            name="audio_file",
            field=models.FileField(blank=True, null=True, upload_to=""),
        ),
    ]
