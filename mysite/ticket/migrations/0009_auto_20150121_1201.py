# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0008_estadoobs_obs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soporte',
            name='titulo',
            field=models.CharField(max_length=1000, blank=True),
        ),
    ]
