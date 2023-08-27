# Generated by Django 4.2.4 on 2023-08-27 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoCall', '0025_alter_notification_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='notifications',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='seen',
        ),
        migrations.AddField(
            model_name='notification',
            name='seen',
            field=models.ManyToManyField(related_name='profile', to='videoCall.profile'),
        ),
    ]
