# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_question_question_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='answer_title',
            field=models.CharField(default='Default as this was added prior to DB', max_length=500),
            preserve_default=False,
        ),
    ]
