# Generated by Django 4.2.4 on 2023-08-26 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoCall', '0019_remove_recording_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='icon',
            field=models.ImageField(upload_to='icon'),
        ),
    ]
