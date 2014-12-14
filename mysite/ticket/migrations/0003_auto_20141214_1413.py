# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0002_document_asunto1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='asunto1',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
