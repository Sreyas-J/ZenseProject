# Generated by Django 4.2.2 on 2023-08-13 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('videoCall', '0003_roommember'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roommember',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room', to='videoCall.profile'),
        ),
    ]
