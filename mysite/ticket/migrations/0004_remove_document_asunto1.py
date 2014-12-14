# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0003_auto_20141214_1413'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='asunto1',
        ),
    ]
