from django.shortcuts import *
from django.template import RequestContext
from django.contrib.auth import *
from django.contrib.auth.models import Group, User
from django.core import serializers
import simplejson
from django.contrib.auth.decorators import login_required
import csv
from django.http import HttpResponse, HttpResponseRedirect
from ticket.models import *
import datetime
from django.core import serializers
import json  
from ticket.models import Document
from ticket.forms import DocumentForm
from django.core.urlresolvers import reverse
from django.db.models import Max,Count


def webx(request):

	return render(request, 'web/index.html')


def tickets_asignados(request):

	id = request.user.id
	ticket_nuevo= Ticket.objects.filter(estado=1).order_by('-id')
	ticket_preatendido= Soporte.objects.filter(ticket__estado=5,soporte_id=id).values('ticket__cliente','soporte__username','ticket__fecha_inicio','ticket_id','ticket__asunto').annotate(dcount=Max('fecha_inicio')).order_by('-id')
	ticket_atendido= Soporte.objects.filter(ticket__estado=2,soporte_id=id).values('ticket__cliente','soporte__username','ticket__fecha_inicio','ticket_id','ticket__asunto').annotate(dcount=Max('fecha_inicio')).order_by('-id')
	ticket_cerrados= Soporte.objects.filter(ticket__estado=3,soporte_id=id).values('ticket__cliente','soporte__username','ticket__fecha_inicio','ticket_id','ticket__asunto').annotate(dcount=Max('fecha_inicio')).order_by('-id')
	ticket_reasignado= Soporte.objects.filter(ticket__estado=6,soporte_id=id,fecha_fin=None).values('ticket__cliente','soporte__username','ticket__fecha_inicio','ticket_id','ticket__asunto').annotate(dcount=Max('fecha_inicio')).order_by('-id')
		
	print request.user.username


	x=User.objects.get(pk=id)
	grupo =x.groups.get()
	grupo= str(grupo)

	username = request.user.username

	for i in range(len(ticket_preatendido)):

		fit = ticket_preatendido[i]['ticket__fecha_inicio']
		today = datetime.datetime.today()
		x=str(today-fit)
		y=x.split('.')[0]
		ticket_preatendido[i]['dif_fecha']=y

	for i in range(len(ticket_atendido)):

		fit = ticket_atendido[i]['ticket__fecha_inicio']
		today = datetime.datetime.today()
		x=str(today-fit)
		y=x.split('.')[0]
		ticket_atendido[i]['dif_fecha']=y

	for i in range(len(ticket_cerrados)):

		fit = ticket_cerrados[i]['ticket__fecha_inicio']
		today = datetime.datetime.today()
		x=str(today-fit)
		y=x.split('.')[0]
		ticket_cerrados[i]['dif_fecha']=y





	if grupo == 'Soporte':

		noti = Notificaciones.objects.all().order_by('-id')[:8]

	if grupo == 'Clientes':

		noti = Notificaciones.objects.filter(ticket__cliente=request.user.id).order_by('-id')[:8]
		


	return render(request,'tickets_asignados.html', {'ticket_reasignado':ticket_reasignado,'noti':noti,'grupo':grupo,'username':username,'ticket_cerrados':ticket_cerrados,'ticket_atendido':ticket_atendido,'ticket_nuevo':ticket_nuevo,'ticket_preatendido':ticket_preatendido})

def ver_usuario(request,id):

	usuario = User.objects.get(id=id)
	x=User.objects.get(pk=id)
	grupo =x.groups.get()
	grupo=str(grupo)

	return render(request,'ver_usuario.html', {'usuario':usuario,'grupo':grupo})



def agregar_ticket(request):

	id = request.user.id


	x=User.objects.get(pk=id)
	grupo =x.groups.get()
	username = request.user.username
	tipos=Tipo.objects.all()
	grupo= str(grupo)
	documents = Archivo.objects.all()

	
	form = FormTicket()
	form_document = DocumentForm()


	noti = Notificaciones.objects.all().order_by('-id')[:8]

	return render(request,'agregar_ticket.html', {'documents':documents,'form_document':form_document,'noti':noti,'tipos':tipos,'form': form,'username':username,'grupo':grupo})


def realtime(request):

	count= Ticket.objects.count()
	ticket = Ticket.objects.all()
	id = request.user.id
	ticket = Ticket.objects.filter(estado=1).order_by('-id')
	x=User.objects.get(pk=id)
	grupo =x.groups.get()
	grupo=str(grupo)
	username = request.user.username
	tipos=Tipo.objects.all()
	estado_name=str('Nuevos')
	noti = Notificaciones.objects.all().order_by('-id')[:8]

	return render(request, 'realtime.html', {'noti':noti,'count':count,'estado_name':estado_name,'tipos':tipos,'username':username,'ticket':ticket,'grupo':grupo})




def realtime_post(request):

	counter = request.POST['count']
	nsoporte = request.POST['soportez']
	nevento = request.POST['eventox']

	nsoporte_act = Soporte.objects.count()
	counter_act = Ticket.objects.count()
	evento_act = Evento.objects.count()

	id = request.user.id
	x=User.objects.get(pk=id)
	grupo =x.groups.get()
	grupo=str(grupo)
	
	m = {'counter_act': counter_act,'soporte_act':nsoporte_act,'evento_act':evento_act}  
	n = json.dumps(m)  
	
	
	if ((str(counter) != str(counter_act))or(str(nsoporte)!=str(nsoporte_act))or(str(nevento)!=str(evento_act))):

		ticket_nuevo = Ticket.objects.all().order_by('-id')[:1]
		soporte_nuevo = Soporte.objects.all().order_by('-id')[:1]
		evento_nuevo = Evento.objects.all().order_by('-id')[:1]

		


		soporte_nuevo = serializers.serialize("json",soporte_nuevo)
		evento_nuevo = serializers.serialize("json",evento_nuevo)
		data = serializers.serialize("json",ticket_nuevo)


		data = {'grupo':grupo,'id':id,'data' : data, 'n' : n ,'snuevo':soporte_nuevo,'sevento':evento_nuevo}
		data = json.dumps(data)

	
		return HttpResponse(data)
	


	return HttpResponse(n)
		

def ticket(request,estado):

	id = request.user.id
	count= Ticket.objects.count()
	nsoporte = Soporte.objects.count()
	
	soporte = Soporte.objects.filter(fecha_fin=None)


	x=User.objects.get(pk=id)

	grupo =x.groups.get()
	grupo= str(grupo)

	username = request.user.username
	tipos=Tipo.objects.all()
	
	if grupo == 'Clientes':
		
		ticket = Ticket.objects.filter(estado=estado,cliente_id=id).order_by('-id')
	else:
		ticket = Ticket.objects.filter(estado=estado).order_by('-id')

	
	if request.method == 'POST':


		form = FormTicket(request.POST)
		
		username = request.user.username
		asunto = request.POST['asunto']
		tipo = request.POST['tipo']
		descripcion=request.POST['descripcion']

		
		fecha_inicio = datetime.datetime.today()
		#estado 1=Nuevo	2=Atendido 3=Prueba 4=Cerrado
		#tipo 1=Incidencia 2=Requerimento


		c=User.objects.get(pk=id).ticket_set.create(cliente=username,asunto=asunto,tipo_id=1,descripcion=descripcion,fecha_inicio=fecha_inicio,validado=0,estado_id=1)
	
		c.save()

		
	
		return HttpResponseRedirect("/ticket")
	else:
		form = FormTicket()

	if str(estado)=='1': 
		estado_name= 'Nuevos'
	if str(estado)=='2': 
		estado_name= 'Atendidos'
	if str(estado)=='3': 
		estado_name= 'En Prueba'
	if str(estado)=='4': 
		estado_name= 'Cerrados'
	if str(estado)=='5': 
		estado_name= 'Preatendido'
	if str(estado)=='6': 
		estado_name= 'Reasignado'

	event = Evento.objects.count()



	if grupo == 'Soporte':

		noti = Notificaciones.objects.all().order_by('-id')[:8]

	if grupo == 'Clientes':

		noti = Notificaciones.objects.filter(ticket__cliente=request.user.id).order_by('-id')[:8]
		

	return render(request, 'home.html', {'event':event,'noti':noti,'nsoporte':nsoporte,'count':count,'soporte':soporte,'estado_name':estado_name,'tipos':tipos,'form': form,'username':username,'ticket':ticket,'grupo':grupo})

def logeate(request):
 
	return render_to_response('logeate.html', context_instance=RequestContext(request))

def push(request):

	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		if user.is_active:
			login(request, user)
			return HttpResponse(simplejson.dumps('Login')) 
		else:
			return HttpResponse(simplejson.dumps('Desactivado')) 
	else:
		return HttpResponse(simplejson.dumps('Usuario Incorrecto'))




def salir(request):

	logout(request)

	return render_to_response('logeate.html', context_instance=RequestContext(request))



def editar_ticket(request,id):
	
	ticket= Ticket.objects.get(id=id)
	form = FormTicket()
	tipos=Tipo.objects.all()
	if request.method == 'POST':


		form = FormTicket(request.POST)
		username = request.user.username
		asunto = request.POST['asunto']
		tipo = request.POST['tipo']
		
		descripcion=request.POST['descripcion']
		fecha_inicio = datetime.datetime.today()

		ticket.asunto = asunto
		ticket.tipo_id =tipo
		ticket.descripcion = descripcion
		ticket.fecha_inicio =fecha_inicio
		ticket.save()
		return HttpResponseRedirect("/ticket")



	return render(request, 'editar_ticket.html', {'form': form,'ticket':ticket,'tipos':tipos})


def atender(request,id):

	ticket= Ticket.objects.get(id=id)
	ticket_pendiente = Ticket.objects.filter(estado=1).order_by('-id')
	username = request.user.username
	id_soporte = request.user.id
	tipos=Tipo.objects.all()
	
	x=User.objects.get(username=username)
	
	grupo =x.groups.get()
	grupo= str(grupo)
	fecha_inicio = datetime.datetime.today()

	if ticket.estado_id ==1 :

		soporte=ticket.soporte_set.create(fecha_inicio=fecha_inicio,soporte_id=id_soporte)
		ticket.estado_id = 2
		ticket.save()

		noti=ticket.notificaciones_set.create(name='Ticket atendido -',fecha_inicio=fecha_inicio)
		noti.save()
		
		return HttpResponseRedirect("/tickets_asignados")

	if ticket.estado_id ==5 :

		ticket.estado_id = 2
		ticket.save()

		noti=ticket.notificaciones_set.create(name='Ticket atendido -',fecha_inicio=fecha_inicio)
		noti.save()

	if ticket.estado_id ==6 :

		ticket.estado_id = 2
		ticket.save()

		noti=ticket.notificaciones_set.create(name='Ticket reatendido -',fecha_inicio=fecha_inicio)
		noti.save()


	return HttpResponseRedirect("/tickets_asignados")

def cerrar(request,id):

	ticket= Ticket.objects.get(id=id)
	ticket.estado_id = 3
	ticket.save()

	return HttpResponseRedirect("/tickets_asignados")



def reasignar(request,id,id_ticket):

	id_ticket= str(id_ticket)
	ticket = Ticket.objects.get(id=id_ticket)
	ticket.estado_id=6
	ticket.save()

	soporte= Soporte.objects.get(id=id)
	user_soporte = User.objects.filter(groups__name='Soporte')


	username = request.user.username
	tipo=Tipo.objects.all()
	x=User.objects.get(username=username)
	
	grupo =x.groups.get()
	grupo= str(grupo)

	return render(request,'reasignar.html', {'id_ticket':id_ticket ,'user_soporte':user_soporte,'soporte':soporte,'username':username,'grupo':grupo,'tipo':tipo})

def asignar_gilda(request,id_ticket):

	

	ticket = Ticket.objects.get(id=id_ticket)
	user_soporte = User.objects.filter(groups__name='Soporte')

	username = request.user.username
	tipo=Tipo.objects.all()
	x=User.objects.get(username=username)
	
	grupo =x.groups.get()
	grupo= str(grupo)

	return render(request,'asignar_gilda.html', {'ticket':ticket,'user_soporte':user_soporte,'username':username,'grupo':grupo,'tipo':tipo})


def reasignar_gilda(request,id_ticket):

	

	ticket = Ticket.objects.get(id=id_ticket)
	ticket.estado_id=6
	ticket.save()

	soporte = ticket.soporte_set.all().values('id').annotate(dcount=Max('fecha_inicio'))
	soporte = soporte[0]['id']
	user_soporte = User.objects.filter(groups__name='Soporte')

	username = request.user.username
	tipo=Tipo.objects.all()
	x=User.objects.get(username=username)
	
	grupo =x.groups.get()
	grupo= str(grupo)

	return render(request,'reasignar_gilda.html', {'soporte':soporte,'ticket':ticket,'user_soporte':user_soporte,'username':username,'grupo':grupo,'tipo':tipo})


def gilda(request):

	ticket_nuevo= Ticket.objects.filter(estado=1).values('id','asunto','fecha_inicio').order_by('-id')
	ticket_atendido= Soporte.objects.filter(ticket__estado=2).values('soporte','soporte__username','ticket__fecha_inicio','ticket_id','ticket__asunto').annotate(dcount=Max('fecha_inicio')).order_by('-id')
	ticket_preatendido= Soporte.objects.filter(ticket__estado=5).values('soporte__username','ticket__fecha_inicio','ticket_id','ticket__asunto').annotate(dcount=Max('fecha_inicio')).order_by('-id')
	ticket_cerrados= Soporte.objects.filter(ticket__estado=3).values('soporte__username','ticket__fecha_inicio','ticket_id','ticket__asunto').annotate(dcount=Max('fecha_inicio')).order_by('-id')
	ticket_reasignado= Soporte.objects.filter(ticket__estado=6,fecha_fin=None).values('ticket__cliente','soporte__username','ticket__fecha_inicio','ticket_id','ticket__asunto').annotate(dcount=Max('fecha_inicio')).order_by('-id')
	
	for i in range(len(ticket_nuevo)):

		fit = ticket_nuevo[i]['fecha_inicio']
		today = datetime.datetime.today()
		x=str(today-fit)
		y=x.split('.')[0]
		
		
		
		ticket_nuevo[i]['dif_fecha']=y
		
	for i in range(len(ticket_preatendido)):

		fit = ticket_preatendido[i]['ticket__fecha_inicio']
		today = datetime.datetime.today()
		x=str(today-fit)
		y=x.split('.')[0]
	
		ticket_preatendido[i]['dif_fecha']=y
		

	for i in range(len(ticket_atendido)):

		fit = ticket_atendido[i]['ticket__fecha_inicio']
	
		today = datetime.datetime.today()
		x=str(today-fit)
		y=x.split('.')[0]

		ticket_atendido[i]['dif_fecha']=y

	for i in range(len(ticket_reasignado)):

		fit = ticket_reasignado[i]['ticket__fecha_inicio']
	
		today = datetime.datetime.today()
		x=str(today-fit)
		y=x.split('.')[0]

		ticket_reasignado[i]['dif_fecha']=y

	for i in range(len(ticket_cerrados)):

		fit = ticket_cerrados[i]['ticket__fecha_inicio']
	
		today = datetime.datetime.today()
		x=str(today-fit)
		y=x.split('.')[0]

	
 		
		ticket_cerrados[i]['dif_fecha']=y
		
		

		
	
	user_soporte = User.objects.filter(groups__name='Soporte')

	username = request.user.username
	tipo=Tipo.objects.all()
	x=User.objects.get(username=username)
	
	grupo =x.groups.get()
	grupo= str(grupo)

	return render(request,'gilda.html', {'ticket_reasignado':ticket_reasignado,'ticket_cerrados':ticket_cerrados,'ticket_preatendido':ticket_preatendido,'ticket_atendido':ticket_atendido,'ticket_nuevo':ticket_nuevo,'user_soporte':user_soporte,'username':username,'grupo':grupo,'tipo':tipo})




def asignar_post_gilda_new(request,soporte,ticket):

	user_soporte = User.objects.get(id=soporte)
	fecha_inicio = datetime.datetime.today()
	ticket = Ticket.objects.get(id=ticket)
	ticket.estado_id = 5
	ticket.soporte_actual = str(user_soporte.username)
	ticket.save()

	ticket.soporte_set.create(fecha_inicio=fecha_inicio,soporte_id=soporte)
	noti=ticket.notificaciones_set.create(name='Ticket by cellphone',fecha_inicio=fecha_inicio)
	noti.save()

	return HttpResponseRedirect("/gilda")




def reasignar_post_gilda_new(request,soporte_act,ticket,soporte):



	sa = Soporte.objects.get(id=soporte_act)
	print sa
	
	sa.fecha_fin = datetime.datetime.today()
	sa.soporte_id = soporte

	sa.save()

	user_soporte = User.objects.get(id=soporte)
	

	fecha_inicio = datetime.datetime.today()

	ticket = Ticket.objects.get(id=ticket)
	ticket.estado_id = 5
	ticket.soporte_actual = str(user_soporte.username)
	ticket.save()


	noti=ticket.notificaciones_set.create(name='Ticket by cellphone',fecha_inicio=fecha_inicio)
	noti.save()
	

	return HttpResponseRedirect("/gilda")





def reasignar_add(request):

	if request.method == 'POST':

		form = FormTicket(request.POST)
		username = request.user.username
		soporte_user = request.POST['soporte']
		
		id_ticket = request.POST['id_ticket']
		ticket = Ticket.objects.get(id=id_ticket)

		id = request.POST['id']
		fecha_inicio = datetime.datetime.today()
		soporte = Soporte.objects.get(id=id)
		fecha_fin = datetime.datetime.today()
		soporte.fecha_fin = fecha_fin

		soporte.save()



		ticket.soporte_set.create(fecha_inicio=fecha_fin,soporte_id=soporte_user)


		noti=ticket.notificaciones_set.create(name='Ticket reasignado ',fecha_inicio=fecha_inicio)
		noti.save()

		return HttpResponseRedirect("/detalle_ticket/"+id_ticket+"/")



def ver_ticket(request,id):

	ticket= Ticket.objects.get(id=id)
	username = request.user.username
	
	x=User.objects.get(username=username)
	grupo =x.groups.get()
	grupo= str(grupo)


	return render(request, 'detalle.html', {'username':username,'grupo':grupo,'tipos':tipos,'ticket':ticket})


def validar(request,id):

	ticket= Ticket.objects.get(id=id)
	ticket.estado_id = 4
	fecha_fin = datetime.datetime.today()
	ticket.fecha_fin = fecha_fin
	
	ticket.save()

	return HttpResponseRedirect("/tickets_asignados")

def detalle_ticket(request,id):

	ticket= Ticket.objects.get(id=id)
	soportes = ticket.soporte_set.all()

	ticket.save()
	username = request.user.username
	tipos=Tipo.objects.all()
	x=User.objects.get(username=username)
	grupo =x.groups.get()
	grupo= str(grupo)
	estado= str(ticket.estado)


	if grupo == 'Soporte':

		noti = Notificaciones.objects.all().order_by('-id')[:8]

	if grupo == 'Clientes':

		noti = Notificaciones.objects.filter(ticket__cliente=request.user.id).order_by('-id')[:8]
		
	
	event = Evento.objects.count()

	return render(request, 'detalle_ticket.html', {'estado':estado,'event':event,'noti':noti,'soportes':soportes,'username':username,'grupo':grupo,'tipos':tipos,'ticket':ticket})

def evento(request,id,id_ticket):

	soporte = Soporte.objects.get(id=id)
	ticket = Ticket.objects.get(id=id_ticket)
	#soporte.evento_set.create(fecha_inicio=fecha_inicio,name=name)

	return render(request, 'evento_add.html', {'ticket':ticket,'soporte':soporte})

def evento_add(request):

	
	if request.method == 'POST':

		evento_id = request.POST['id_ticket']
		soporte_id = request.POST['id']
		user = 	request.user.id	
		name = request.POST['name']
		fecha_inicio = datetime.datetime.today()

		ix = request.POST['cont']		

		for i in range (1, int(ix)+1):
		
			newdoc = Document(docfile = request.FILES['docfile'+str(i)],ticket_id=evento_id)
			newdoc.save()

		
		soporte = Soporte.objects.get(id=soporte_id)
		soporte.evento_set.create(fecha_inicio=fecha_inicio,name=name,user_id=user)

		noti=soporte.ticket.notificaciones_set.create(name='Ticket evento ',fecha_inicio=fecha_inicio)
		noti.save()

		return HttpResponseRedirect("/ver_evento/"+soporte_id+"/"+evento_id)

def ver_evento(request,id,id_ticket):

	ticket = Ticket.objects.get(id=id_ticket)
	soporte = Soporte.objects.get(id=id)
	evento = soporte.evento_set.all()
	event = Evento.objects.count()
	noti = Notificaciones.objects.all().order_by('-id')[:8]
	soporte_abierto = Soporte.objects.filter(fecha_fin=None)

	username = request.user.username
	tipos=Tipo.objects.all()
	x=User.objects.get(username=username)
	grupo =x.groups.get()
	grupo= str(grupo)
	estado= str(ticket.estado)

	return render(request, 'ver_evento.html', {'estado':estado,'grupo':grupo,'username':username,'soporte_abierto':soporte_abierto,'noti':noti,'event':event,'evento':evento,'soporte':soporte,'ticket':ticket})


def realtime_post_monitor(request):

	counter = request.POST['count']

	Ticket.objects.all().order_by('-id')[:1]



	counter_act = Ticket.objects.count()
	m = {'counter_act': counter_act}  
	n = json.dumps(m)  
	

	
	if (str(counter) != str(counter_act)):


		
		ticket_nuevo = Ticket.objects.all().order_by('-id')[:1]
		data = serializers.serialize("json",ticket_nuevo)
		data = { 'data' : data, 'n' : n }
		data = json.dumps(data)

		
		return HttpResponse(data)
	


	return HttpResponse(n)


def notificaciones(request):

	
	username = request.user.username


	x=User.objects.get(username=username)
	grupo =x.groups.get()
	grupo= str(grupo)
	

	if grupo == 'Soporte':

		noti = Notificaciones.objects.all().order_by('-id')[:8]

	if grupo == 'Clientes':

		noti = Notificaciones.objects.filter(ticket__cliente=request.user.id).order_by('-id')[:8]
	
	return render(request, 'notificaciones.html', {'noti':noti,'grupo':grupo,'username':username})


def agregar_ticket(request):
    # Handle file upload

	id = request.user.id
	ticket = Ticket.objects.filter(estado=1).order_by('-id')
	x=User.objects.get(pk=id)
	grupo =x.groups.get()
	grupo=str(grupo)
	username = request.user.username
	tipos=Tipo.objects.all()
	estado_name=str('Nuevos')


	
	if request.method == 'POST':

	
		form = DocumentForm(request.POST, request.FILES)

		username = request.user.username
		asunto = request.POST['asunto']
		tipo = request.POST['tipo']
		descripcion=request.POST['descripcion']

		fecha_inicio = datetime.datetime.today()

		print fecha_inicio
		#estado 1=Nuevo	2=Atendido 3=Prueba 4=Cerrado
		#tipo 1=Incidencia 2=Requerimento


		c=User.objects.get(pk=id).ticket_set.create(cliente=username,asunto=asunto,tipo_id=1,descripcion=descripcion,fecha_inicio=fecha_inicio,estado_id=1)
		
		c.save()


		noti=c.notificaciones_set.create(name='Ticket nuevo ',fecha_inicio=fecha_inicio)
		noti.save()

		ix = request.POST['cont']		

		for i in range (1, int(ix)+1):
		
			newdoc = Document(docfile = request.FILES['docfile'+str(i)],ticket_id=c.id,user_id=id)
			newdoc.save()

		
            # Redirect to the document list after POST
		return HttpResponseRedirect("/ticket/1")
	else:
		form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
	documents = Document.objects.all()
	noti = Notificaciones.objects.all().order_by('-id')[:8]

    # Render list page with the documents and the form
	return render_to_response(
        'agregar_ticket.html',
        {'noti':noti,'tipos':tipos,'documents': documents, 'form': form,'username':username,'grupo':grupo},
        context_instance=RequestContext(request)
    )

def documentos(request,id_ticket):

	ticket = Ticket.objects.get(id=id_ticket)
	username = request.user.username
	
	noti = Notificaciones.objects.all().order_by('-id')[:8]
	x=User.objects.get(username=username)
	grupo =x.groups.get()
	grupo= str(grupo)

	documentos = Document.objects.filter(ticket=id_ticket)

	cumentos = Document.objects.all()

	

	return render(request, 'documentos.html', {'documentos':documentos,'grupo':grupo,'noti':noti,'username':username,'ticket':ticket})


def list1(request):

	if request.method == 'POST':

		id = request.user.id
		form = DocumentForm(request.POST, request.FILES)
		ticket = request.POST['ticket']
		print ticket
		username = request.user.username
		c= Ticket.objects.get(id=ticket)

		fecha_inicio = datetime.datetime.today()
		#estado 1=Nuevo	2=Atendido 3=Prueba 4=Cerrado 5 =Preatendido
		#tipo 1=Incidencia 2=Requerimento


		noti=c.notificaciones_set.create(name='Archivo nuevo ',fecha_inicio=fecha_inicio)
		noti.save()

		ix = request.POST['cont']
			

		for i in range (1, int(ix)+1):
		
			newdoc = Document(docfile = request.FILES['docfile'+str(i)],ticket_id=c.id,user_id=id)
			newdoc.save()

		
            # Redirect to the document list after POST
		return HttpResponseRedirect("/documentos/"+str(ticket))
	
