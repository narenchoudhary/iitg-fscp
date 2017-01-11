# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-11 21:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20161217_0202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='discipline',
            field=models.CharField(choices=[(b'Aerodynamics and Propulsion', b'Aerodynamics and Propulsion'), (b'Biotechnology', b'Biotechnology'), (b'CAM', b'CAM'), (b'Chemical Engineering', b'Chemical Engineering'), (b'Chemical Science and Technology', b'Chemical Science and Technology'), (b'Chemistry', b'Chemistry'), (b'Civil Engineering', b'Civil Engineering'), (b'Communication Engineering', b'Communication Engineering'), (b'Computational Mechanics', b'Computational Mechanics'), (b'Computer Science and Engineering', b'Computer Science and Engineering'), (b'Design', b'Design'), (b'Development Studies', b'Development Studies'), (b'Electronics and Communication Engineering', b'Electronics and Communication Engineering'), (b'Electronics and Electrical Engineering', b'Electronics and Electrical Engineering'), (b'Energy', b'Energy'), (b'Engineering Physics', b'Engineering Physics'), (b'Environmental Engineering', b'Environmental Engineering'), (b'Fluids and Thermal', b'Fluids and Thermal'), (b'GeoTechnical Engineering', b'GeoTechnical Engineering'), (b'Infrastructure Engineering and Management', b'Infrastructure Engineering and Management'), (b'Machine Design', b'Machine Design'), (b'Material Science and Technology', b'Material Science and Technology'), (b'Mathematics and Computing', b'Mathematics and Computing'), (b'Mechanical Engineering', b'Mechanical Engineering'), (b'Petroleum Science and Technology', b'Petroleum Science and Technology'), (b'Physics', b'Physics'), (b'Power and Control', b'Power and Control'), (b'RF and Photonics', b'RF and Photonics'), (b'Signal Processing', b'Signal Processing'), (b'Structural Engineering', b'Structural Engineering'), (b'Theoretical Computer Science', b'Theoretical Computer Science'), (b'Transportation Engineering', b'Transportation Engineering'), (b'VLSI', b'VLSI'), (b'Water Resources Engineering', b'Water Resources Engineering')], max_length=200, verbose_name='Major Discipline'),
        ),
    ]
