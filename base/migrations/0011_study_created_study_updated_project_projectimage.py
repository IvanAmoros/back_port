# Generated by Django 5.0.2 on 2024-03-28 01:10

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_alter_technicalskill_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='study',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='study',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tittle', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=1000)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('skills', models.ManyToManyField(blank=True, to='base.technicalskill')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='project_images/')),
                ('caption', models.CharField(blank=True, max_length=255)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='base.project')),
            ],
        ),
    ]