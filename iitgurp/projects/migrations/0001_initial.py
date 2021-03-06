# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-16 23:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70)),
                ('description', models.CharField(blank=True, max_length=300, null=True)),
                ('hours_per_week', models.DecimalField(decimal_places=1, default=2, max_digits=3, verbose_name='Hours Per Week')),
                ('start_date', models.DateField(null=True, verbose_name='Tentative Start Date')),
                ('end_date', models.DateField(null=True, verbose_name='Tentative End Date')),
                ('requirements', models.TextField(blank=True, max_length=400, null=True, verbose_name='Other Requirements')),
                ('creation_datetime', models.DateTimeField(blank=True, null=True)),
                ('last_updated', models.DateField(blank=True, null=True)),
                ('closing_datetime', models.DateTimeField(blank=True, help_text='Applications will close after this date.', null=True, verbose_name='Closing Date')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deletion_datetime', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-closing_datetime'],
            },
        ),
        migrations.CreateModel(
            name='ProjectStudentRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_datetime', models.DateTimeField()),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
                ('is_shortlisted', models.NullBooleanField(default=None)),
                ('shortlist_datetime', models.DateTimeField(blank=True, null=True)),
                ('is_completed', models.NullBooleanField(default=None)),
                ('completion_datetime', models.DateTimeField(blank=True, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.Student')),
            ],
            options={
                'ordering': ['last_updated'],
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True)),
                ('description', models.CharField(max_length=600, null=True)),
                ('created_on', models.DateTimeField(blank=True)),
                ('last_updated_on', models.DateTimeField(blank=True)),
            ],
            options={
                'ordering': ['name'],
                'get_latest_by': 'last_updated_on',
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.AddField(
            model_name='project',
            name='applicants',
            field=models.ManyToManyField(through='projects.ProjectStudentRelation', to='profiles.Student'),
        ),
        migrations.AddField(
            model_name='project',
            name='faculty',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.Faculty'),
        ),
        migrations.AddField(
            model_name='project',
            name='skills',
            field=models.ManyToManyField(blank=True, to='projects.Skill', verbose_name='Tags'),
        ),
        migrations.AlterUniqueTogether(
            name='projectstudentrelation',
            unique_together=set([('project', 'student')]),
        ),
    ]
