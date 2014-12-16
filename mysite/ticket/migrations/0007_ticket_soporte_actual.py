# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import __builtin__


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0006_auto_20141215_1934'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='soporte_actual',
            field=models.CharField(default=__builtin__.int, max_length=100, blank=True),
            preserve_default=False,
        ),
    ]
