# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0005_document_asunto1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='name',
            field=models.CharField(max_length=1000, blank=True),
        ),
    ]
