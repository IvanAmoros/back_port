# Generated by Django 5.0.2 on 2024-03-25 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_remove_technicalskill_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='technicalskill',
            name='logo',
            field=models.ImageField(null=True, upload_to=None),
        ),
    ]
