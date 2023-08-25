# Generated by Django 4.2.4 on 2023-08-24 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoCall', '0010_remove_profile_doc_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recording',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='records',
            field=models.ManyToManyField(related_name='room', to='videoCall.recording'),
        ),
        migrations.AddField(
            model_name='profile',
            name='recordings',
            field=models.ManyToManyField(related_name='recorder', to='videoCall.recording'),
        ),
    ]