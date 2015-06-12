# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_auto_20150610_0121'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gender',
            options={'verbose_name_plural': 'Gender'},
        ),
        migrations.AlterModelOptions(
            name='occupation',
            options={'verbose_name_plural': 'Occupation'},
        ),
        migrations.AlterModelOptions(
            name='ratings',
            options={'verbose_name_plural': 'Ratings'},
        ),
    ]
