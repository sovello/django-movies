# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_auto_20150609_1853'),
    ]

    operations = [
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
    ]
