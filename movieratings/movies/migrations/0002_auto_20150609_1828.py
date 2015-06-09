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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('rating', models.IntegerField()),
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
            model_name='movie',
            name='genre',
        ),
        migrations.AddField(
            model_name='movie',
            name='genre',
            field=models.ManyToManyField(to='movies.Genre'),
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
