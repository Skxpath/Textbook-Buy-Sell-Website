# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-17 07:17
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
            name='Ad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('condition', models.CharField(choices=[('NEW', 'New'), ('GOOD', 'Good'), ('FAIR', 'Fair'), ('WORN', 'Worn'), ('BAD', 'Bad')], default='GOOD', max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='Textbook',
            fields=[
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('isbn', models.DecimalField(decimal_places=0, max_digits=13, primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='ad',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='textbook_app.Textbook'),
        ),
        migrations.AddField(
            model_name='ad',
            name='poster',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]