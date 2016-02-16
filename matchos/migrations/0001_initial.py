# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-07 21:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team1', models.CharField(max_length=50)),
                ('team2', models.CharField(max_length=50)),
                ('score', models.IntegerField()),
                ('date', models.CharField(max_length=50)),
            ],
        ),
    ]