# Generated by Django 5.0.1 on 2024-02-05 16:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_technicalskill_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='technicalskill',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.technicalskillcategory'),
        ),
    ]
