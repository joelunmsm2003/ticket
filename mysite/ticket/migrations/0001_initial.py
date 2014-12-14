# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Archivo',
            fields=[
                ('id', models.AutoField(max_length=100, serialize=False, primary_key=True)),
                ('docfile', models.FileField(upload_to=b'/')),
                ('asunto', models.CharField(max_length=100, blank=True)),
                ('fecha_inicio', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(max_length=100, serialize=False, primary_key=True)),
                ('docfile', models.FileField(upload_to=b'files')),
                ('detalle', models.CharField(max_length=100, blank=True)),
                ('asunto', models.CharField(max_length=100, blank=True)),
                ('fecha_inicio', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, blank=True)),
                ('fecha_inicio', models.DateTimeField(null=True, blank=True)),
                ('comentario', models.CharField(max_length=100, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.AutoField(max_length=100, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100, blank=True)),
                ('fecha_inicio', models.DateTimeField(null=True, blank=True)),
                ('comentario', models.CharField(max_length=100, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notificaciones',
            fields=[
                ('id', models.AutoField(max_length=100, serialize=False, primary_key=True)),
                ('tipo', models.CharField(max_length=100, blank=True)),
                ('name', models.CharField(max_length=100, blank=True)),
                ('fecha_inicio', models.DateTimeField(null=True, blank=True)),
                ('comentario', models.CharField(max_length=100, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Soporte',
            fields=[
                ('id', models.AutoField(max_length=100, serialize=False, primary_key=True)),
                ('titulo', models.CharField(max_length=100, blank=True)),
                ('fecha_inicio', models.DateTimeField()),
                ('fecha_fin', models.DateTimeField(null=True, blank=True)),
                ('comentario', models.CharField(max_length=100, blank=True)),
                ('soporte', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(max_length=100, serialize=False, primary_key=True)),
                ('asunto', models.CharField(max_length=100, blank=True)),
                ('descripcion', models.CharField(max_length=100, blank=True)),
                ('fecha_inicio', models.DateTimeField()),
                ('fecha_fin', models.DateTimeField(null=True, blank=True)),
                ('comentario', models.CharField(max_length=100, blank=True)),
                ('cliente', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('estado', models.ForeignKey(to='ticket.Estado')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tipo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, blank=True)),
                ('fecha_inicio', models.DateTimeField(null=True, blank=True)),
                ('comentario', models.CharField(max_length=100, blank=True)),
                ('comentario1', models.CharField(max_length=100, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='ticket',
            name='tipo',
            field=models.ForeignKey(to='ticket.Tipo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='soporte',
            name='ticket',
            field=models.ForeignKey(to='ticket.Ticket'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='notificaciones',
            name='ticket',
            field=models.ForeignKey(to='ticket.Ticket'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='evento',
            name='evento',
            field=models.ForeignKey(to='ticket.Soporte'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='evento',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='ticket',
            field=models.ForeignKey(to='ticket.Ticket'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='archivo',
            name='ticket',
            field=models.ForeignKey(to='ticket.Ticket'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='archivo',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
