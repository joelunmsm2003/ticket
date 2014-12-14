# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0004_remove_document_asunto1'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='asunto1',
            field=models.CharField(default=datetime.date(2014, 12, 14), max_length=100, blank=True),
            preserve_default=False,
        ),
    ]
