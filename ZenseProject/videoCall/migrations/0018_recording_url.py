# Generated by Django 4.2.4 on 2023-08-26 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoCall', '0017_group_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='recording',
            name='url',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
