# Generated by Django 5.0.2 on 2024-05-17 16:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('film_festival', '0004_alter_film_imdb_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='proposed_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='proposed_films', to=settings.AUTH_USER_MODEL),
        ),
    ]
