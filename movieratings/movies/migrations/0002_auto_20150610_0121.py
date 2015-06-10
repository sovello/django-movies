# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ratings',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('rating', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='ratingdata',
            name='movie',
        ),
        migrations.RemoveField(
            model_name='ratingdata',
            name='rater',
        ),
        migrations.RemoveField(
            model_name='genre',
            name='id',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='id',
        ),
        migrations.RemoveField(
            model_name='occupation',
            name='id',
        ),
        migrations.AddField(
            model_name='genre',
            name='genre_id',
            field=models.IntegerField(primary_key=True, serialize=False, default=0),
        ),
        migrations.AddField(
            model_name='movie',
            name='movie_id',
            field=models.IntegerField(primary_key=True, verbose_name='Movie ID', serialize=False, default=10000),
        ),
        migrations.AddField(
            model_name='occupation',
            name='occupation_id',
            field=models.CharField(primary_key=True, default=1, serialize=False, max_length=100),
        ),
        migrations.AddField(
            model_name='rater',
            name='number',
            field=models.IntegerField(verbose_name='Rater Number', default=10000),
        ),
        migrations.RemoveField(
            model_name='movie',
            name='genre',
        ),
        migrations.AddField(
            model_name='movie',
            name='genre',
            field=models.ManyToManyField(to='movies.Genre'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='imdb_url',
            field=models.CharField(verbose_name='IMDB URL', max_length=250),
        ),
        migrations.AlterField(
            model_name='movie',
            name='release_date',
            field=models.DateField(verbose_name='Release Date'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='title',
            field=models.CharField(verbose_name='Movie Title', max_length=200),
        ),
        migrations.AlterField(
            model_name='movie',
            name='video_release_date',
            field=models.DateField(verbose_name='Video Release Date'),
        ),
        migrations.AlterField(
            model_name='rater',
            name='zip_code',
            field=models.CharField(verbose_name='Zip Code', max_length=20),
        ),
        migrations.DeleteModel(
            name='RatingData',
        ),
        migrations.AddField(
            model_name='ratings',
            name='movie',
            field=models.ForeignKey(to='movies.Movie'),
        ),
        migrations.AddField(
            model_name='ratings',
            name='rater',
            field=models.ForeignKey(to='movies.Rater'),
        ),
    ]
