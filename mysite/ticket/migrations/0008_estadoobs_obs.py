# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ticket', '0007_ticket_soporte_actual'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstadoObs',
            fields=[
                ('id', models.AutoField(max_length=100, serialize=False, primary_key=True)),
                ('estado', models.CharField(max_length=100, blank=True)),
                ('fecha', models.DateTimeField(null=True, blank=True)),
                ('comentario', models.CharField(max_length=100, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Obs',
            fields=[
                ('id', models.AutoField(max_length=100, serialize=False, primary_key=True)),
                ('fecha', models.DateTimeField(null=True, blank=True)),
                ('asunto', models.CharField(max_length=100, blank=True)),
                ('descripcion', models.CharField(max_length=100, blank=True)),
                ('estado', models.ForeignKey(to='ticket.Estado')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
