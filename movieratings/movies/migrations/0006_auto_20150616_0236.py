# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_auto_20150612_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occupation',
            name='occupation_id',
            field=models.IntegerField(default=1, max_length=100, primary_key=True, serialize=False),
        ),
    ]
