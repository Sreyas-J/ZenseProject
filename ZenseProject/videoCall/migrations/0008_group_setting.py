# Generated by Django 4.2.4 on 2023-08-23 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoCall', '0007_profile_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='setting',
            field=models.CharField(choices=[('ADMIN', 'ADMIN'), ('EVERYONE', 'EVERYONE')], default='EVERYONE', max_length=15),
            preserve_default=False,
        ),
    ]