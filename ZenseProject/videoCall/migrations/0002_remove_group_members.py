# Generated by Django 4.2.4 on 2023-08-10 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videoCall', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='members',
        ),
    ]
