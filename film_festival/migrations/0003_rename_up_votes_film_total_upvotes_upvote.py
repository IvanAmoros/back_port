# Generated by Django 5.0.2 on 2024-05-16 22:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('film_festival', '0002_rating_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='film',
            old_name='up_votes',
            new_name='total_upvotes',
        ),
        migrations.CreateModel(
            name='Upvote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='upvotes', to='film_festival.film')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_upvotes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'film')},
            },
        ),
    ]