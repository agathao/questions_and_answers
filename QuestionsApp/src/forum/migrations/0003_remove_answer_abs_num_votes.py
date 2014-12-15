# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_answer_abs_num_votes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='abs_num_votes',
        ),
    ]
