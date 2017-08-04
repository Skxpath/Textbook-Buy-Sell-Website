# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-01 03:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('textbook_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('users', models.ManyToManyField(related_name='chats', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.TextField()),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='textbook_app.Chat')),
            ],
        ),
        migrations.AlterField(
            model_name='textbook',
            name='author',
            field=models.CharField(max_length=200, verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='textbook',
            name='description',
            field=models.TextField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='textbook',
            name='isbn',
            field=models.DecimalField(decimal_places=0, max_digits=13, primary_key=True, serialize=False, verbose_name='ISBN'),
        ),
        migrations.AlterField(
            model_name='textbook',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Book Title'),
        ),
    ]
