# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_auto_20150616_0236'),
    ]

    operations = [
        migrations.AddField(
            model_name='rater',
            name='photo',
            field=models.ImageField(null=True, blank=True, upload_to='profile_photos'),
        ),
    ]
