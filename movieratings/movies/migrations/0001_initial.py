# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=140)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('release_date', models.DateField()),
                ('video_release_date', models.DateField()),
                ('imdb_url', models.CharField(max_length=250)),
                ('genre', models.ForeignKey(to='movies.Genre')),
            ],
        ),
        migrations.CreateModel(
            name='Occupation',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=140)),
            ],
        ),
        migrations.CreateModel(
            name='Rater',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('age', models.IntegerField()),
                ('zip_code', models.CharField(max_length=20)),
                ('gender', models.ForeignKey(to='movies.Gender')),
                ('occupation', models.ForeignKey(to='movies.Occupation')),
            ],
        ),
        migrations.CreateModel(
            name='RatingData',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('rating', models.IntegerField()),
                ('movie', models.ForeignKey(to='movies.Movie')),
                ('rater', models.ForeignKey(to='movies.Rater')),
            ],
        ),
    ]
