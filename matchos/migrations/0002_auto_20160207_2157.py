# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-07 21:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matchos', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='match',
            old_name='score',
            new_name='winner',
        ),
    ]
