# Generated by Django 4.2.4 on 2023-08-26 05:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videoCall', '0018_recording_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recording',
            name='url',
        ),
    ]
