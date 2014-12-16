# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0007_answervotesregistry_questionvotesregistry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tags',
            name='question',
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(to='forum.Tags'),
            preserve_default=True,
        ),
    ]
