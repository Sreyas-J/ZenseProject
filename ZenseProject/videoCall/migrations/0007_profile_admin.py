# Generated by Django 4.2.4 on 2023-08-23 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoCall', '0006_alter_group_doc'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='admin',
            field=models.ManyToManyField(related_name='admin_right', to='videoCall.group'),
        ),
    ]
