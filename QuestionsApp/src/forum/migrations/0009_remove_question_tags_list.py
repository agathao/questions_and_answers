# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0008_auto_20141216_0121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='tags_list',
        ),
    ]
