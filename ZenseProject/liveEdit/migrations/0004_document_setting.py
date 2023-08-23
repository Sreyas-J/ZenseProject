# Generated by Django 4.2.4 on 2023-08-23 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liveEdit', '0003_merge_20230816_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='setting',
            field=models.CharField(choices=[('ADMIN', 'ADMIN'), ('EVERYONE', 'EVERYONE')], default='EVERYONE', max_length=15),
            preserve_default=False,
        ),
    ]
