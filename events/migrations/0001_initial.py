# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-10 14:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=500)),
                ('date', models.DateField()),
                ('singles_num', models.IntegerField(default=60)),
                ('singles_approved', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.IntegerField(choices=[(1, 'male'), (2, 'female')])),
                ('status', models.IntegerField(choices=[(1, 'single'), (2, 'divorcee'), (3, 'divorcee with kids')], default=1)),
                ('dob', models.DateField(blank=True, null=True)),
                ('is_cohen', models.BooleanField(default=False)),
                ('picture', models.ImageField(default='/no-image.jpg', upload_to='')),
                ('is_matchmaker', models.BooleanField(default=False)),
                ('is_single', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Profile'),
        ),
    ]
