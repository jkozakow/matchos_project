# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-11 20:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matchos', '0003_team'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchFootball',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('hometeamname', models.CharField(max_length=50)),
                ('hometeamid', models.IntegerField()),
                ('awayteamname', models.CharField(max_length=50)),
                ('awayteamid', models.IntegerField()),
                ('goalshometeam', models.IntegerField()),
                ('goalsawayteam', models.IntegerField()),
                ('date', models.CharField(max_length=50)),
            ],
        ),
    ]