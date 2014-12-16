# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_auto_20141215_0321'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_title',
            field=models.CharField(default='Default title', max_length=500),
            preserve_default=False,
        ),
    ]
