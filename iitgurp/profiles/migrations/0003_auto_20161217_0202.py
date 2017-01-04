# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-17 02:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20161216_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='discipline',
            field=models.CharField(choices=[(b'Computer Science and Engineering', b'Computer Science and Engineering'), (b'CAM', b'CAM'), (b'Chemistry', b'Chemistry'), (b'Electronics and Communication Engineering', b'Electronics and Communication Engineering'), (b'Computational Mechanics', b'Computational Mechanics'), (b'Civil Engineering', b'Civil Engineering'), (b'Design', b'Design'), (b'Energy', b'Energy'), (b'Development Studies', b'Development Studies'), (b'Mathematics and Computing', b'Mathematics and Computing'), (b'Mechanical Engineering', b'Mechanical Engineering'), (b'Environmental Engineering', b'Environmental Engineering'), (b'GeoTechnical Engineering', b'GeoTechnical Engineering'), (b'Biotechnology', b'Biotechnology'), (b'Petroleum Science and Technology', b'Petroleum Science and Technology'), (b'Chemical Engineering', b'Chemical Engineering'), (b'Engineering Physics', b'Engineering Physics'), (b'Electronics and Electrical Engineering', b'Electronics and Electrical Engineering'), (b'Transportation Engineering', b'Transportation Engineering'), (b'Chemical Science and Technology', b'Chemical Science and Technology'), (b'Material Science and Technology', b'Material Science and Technology'), (b'Physics', b'Physics'), (b'Fluids and Thermal', b'Fluids and Thermal'), (b'VLSI', b'VLSI'), (b'Theoretical Computer Science', b'Theoretical Computer Science'), (b'Communication Engineering', b'Communication Engineering'), (b'Signal Processing', b'Signal Processing'), (b'Power and Control', b'Power and Control'), (b'RF and Photonics', b'RF and Photonics'), (b'Machine Design', b'Machine Design'), (b'Water Resources Engineering', b'Water Resources Engineering'), (b'Structural Engineering', b'Structural Engineering'), (b'Aerodynamics and Propulsion', b'Aerodynamics and Propulsion'), (b'Infrastructure Engineering and Management', b'Infrastructure Engineering and Management')], max_length=200, verbose_name='Major Discipline'),
        ),
    ]