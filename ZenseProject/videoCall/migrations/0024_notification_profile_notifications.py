# Generated by Django 4.2.4 on 2023-08-27 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoCall', '0023_alter_group_options_remove_group_updated'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('seen', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='notifications',
            field=models.ManyToManyField(related_name='user_info', to='videoCall.notification'),
        ),
    ]
