from django.db import models
from django.contrib.auth.models import Group, User
from django import forms


class FormTicket(forms.Form):

    cc_myself = forms.BooleanField(required=False)


class Tipo(models.Model):

	name = models.CharField(max_length=100,blank=True)
	fecha_inicio = models.DateTimeField(null=True,blank=True)
	comentario = models.CharField(max_length=100,blank=True)
	comentario1 = models.CharField(max_length=100,blank=True)
	def __str__(self):              # __unicode__ on Python 2
		return self.name

class Estado(models.Model):

	name = models.CharField(max_length=100,blank=True)
	fecha_inicio = models.DateTimeField(null=True,blank=True)
	comentario = models.CharField(max_length=100,blank=True)
	def __str__(self):              # __unicode__ on Python 2
		return self.name

class Ticket(models.Model):

	id = models.AutoField(max_length=100,primary_key=True)
	cliente = models.ForeignKey(User)
	asunto = models.CharField(max_length=100,blank=True)
	tipo = models.ForeignKey(Tipo)
	soporte_actual = models.CharField(max_length=100,blank=True)
	descripcion = models.CharField(max_length=100,blank=True)
	fecha_inicio = models.DateTimeField()
	fecha_fin = models.DateTimeField(null=True,blank=True)
	estado = models.ForeignKey(Estado)
	
	comentario = models.CharField(max_length=100,blank=True)
	def __str__(self):              # __unicode__ on Python 2
		return self.asunto

class Soporte(models.Model):

	id = models.AutoField(max_length=100,primary_key=True)
	ticket = models.ForeignKey(Ticket)
	titulo = models.CharField(max_length=100,blank=True)
	fecha_inicio = models.DateTimeField()
	fecha_fin= models.DateTimeField(null=True,blank=True)
	soporte = models.ForeignKey(User,)
	
	comentario = models.CharField(max_length=100,blank=True)
	

	def __str__(self):              # __unicode__ on Python 2
		return self.titulo

class Evento(models.Model):

	id = models.AutoField(max_length=100,primary_key=True)
	evento = models.ForeignKey(Soporte)
	user = models.ForeignKey(User,)
	name = models.CharField(max_length=1000,blank=True)
	fecha_inicio = models.DateTimeField(null=True,blank=True)
	comentario = models.CharField(max_length=100,blank=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name


class Notificaciones(models.Model):

	id = models.AutoField(max_length=100,primary_key=True)
	ticket = models.ForeignKey(Ticket)
	tipo =models.CharField(max_length=100,blank=True)
	name = models.CharField(max_length=100,blank=True)
	fecha_inicio = models.DateTimeField(null=True,blank=True)
	comentario = models.CharField(max_length=100,blank=True)

	def __str__(self):              # __unicode__ on Python 2
		return self.name


class Document(models.Model):

	id = models.AutoField(max_length=100,primary_key=True)
	docfile = models.FileField(upload_to='files')
	ticket = models.ForeignKey(Ticket)
	detalle = models.CharField(max_length=100,blank=True)
	user = models.ForeignKey(User,)
	asunto = models.CharField(max_length=100,blank=True)
	asunto1 = models.CharField(max_length=100,blank=True)
	fecha_inicio = models.DateTimeField(null=True,blank=True)

class Archivo(models.Model):
	
	id = models.AutoField(max_length=100,primary_key=True)
	ticket = models.ForeignKey(Ticket)
	docfile = models.FileField(upload_to='/')
	asunto =models.CharField(max_length=100,blank=True)
	asunto =models.CharField(max_length=100,blank=True)
	user = models.ForeignKey(User,)
	fecha_inicio = models.DateTimeField(null=True,blank=True)
















