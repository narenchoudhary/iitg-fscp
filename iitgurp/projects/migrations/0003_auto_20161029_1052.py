# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-29 10:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
        ('projects', '0002_auto_20161029_1035'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='creation_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='faculty',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.Faculty'),
        ),
        migrations.AddField(
            model_name='project',
            name='last_updated',
            field=models.DateField(blank=True, null=True),
        ),
    ]