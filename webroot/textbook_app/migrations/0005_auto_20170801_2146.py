# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-01 21:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('textbook_app', '0004_merge_20170801_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textbook',
            name='description',
            field=models.TextField(verbose_name='Textbook Description'),
        ),
    ]
