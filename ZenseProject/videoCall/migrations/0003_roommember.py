# Generated by Django 4.2.2 on 2023-08-10 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoCall', '0002_remove_group_members'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('uid', models.CharField(max_length=5)),
                ('room', models.CharField(max_length=100)),
            ],
        ),
    ]
