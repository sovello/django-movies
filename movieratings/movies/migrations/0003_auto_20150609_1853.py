# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_auto_20150609_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='imdb_url',
            field=models.CharField(max_length=250, verbose_name='IMDB URL'),
        ),
    ]
