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
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def webx(request):

	return render(request, 'web/index.html')


def ticketscerrados(request):

	username = request.user.username
	
	id = request.user.id
	x=User.objects.get(pk=id)
	grupo =x.groups.get()
	grupo=str(grupo)

	if grupo=='Soporte' :

		ticket = Ticket.objects.filter(estado_id=4,soporte_actual=username).order_by('-fecha_fin')

	if grupo=='Clientes' :

		ticket = Ticket.objects.filter(estado_id=4,cliente_id=id).order_by('-fecha_fin')


	paginator = Paginator(ticket, 20) # Show 25 contacts per page

	page = request.GET.get('page')

	try:
		contacts = paginator.page(page)
	except PageNotAnInteger:
    # If page is not an integer, deliver first page.
		contacts = paginator.page(1)
	except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
		contacts = paginator.page(paginator.num_pages)


	return render(request,'ticketscerrados.html', {'username':username,'grupo':grupo,'contacts':contacts})


def email(request):

	send_mail('MailGun works great!', 'It really really does.', 'xienwork@sandboxbb5414fe26d94969aa76e2ece53f668e.mailgun.org', ['joelunmsm@gmail.com'], fail_silently=False)
	return render(request, 'email.html')


def tickets_asignados(request):

	id = request.user.id
	ticket_nuevo= Ticket.objects.filter(estado=1).order_by('-id')
	ticket_preatendido= Soporte.objects.filter(ticket__estado=5,soporte_id=id).values('ticket__cliente__username','soporte__username','ticket__fecha_inicio','ticket_id','ticket__asunto').annotate(dcount=Max('fecha_inicio')).order_by('-id')
	ticket_atendido= Soporte.objects.filter(ticket__estado=2,soporte_id=id).values('ticket__cliente__username','soporte__username','ticket__fecha_inicio','ticket_id','ticket__asunto').annotate(dcount=Max('fecha_inicio')).order_by('-id')
	ticket_cerrados= Soporte.objects.filter(ticket__estado=3,soporte_id=id).values('ticket__cliente__username','soporte__username','ticket__fecha_inicio','ticket_id','ticket__asunto').annotate(dcount=Max('fecha_inicio')).order_by('-id')
	ticket_reasignado= Soporte.objects.filter(ticket__estado=6,soporte_id=id,fecha_fin=None).values('ticket__cliente__username','soporte__username','ticket__fecha_inicio','ticket_id','ticket__asunto').annotate(dcount=Max('fecha_inicio')).order_by('-id')
		
	print request.user.username


	x=User.objects.get(pk=id)
	grupo =x.groups.get()
	grupo= str(grupo)

	username = request.user.username
	first_name = request.user.first_name

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

	for i in range(len(ticket_reasignado)):

		fit = ticket_reasignado[i]['ticket__fecha_inicio']
		today = datetime.datetime.today()
		x=str(today-fit)
		y=x.split('.')[0]
		ticket_reasignado[i]['dif_fecha']=y

	if grupo == 'Soporte':

		noti = Notificaciones.objects.all().order_by('-id')[:8]

	if grupo == 'Clientes':

		noti = Notificaciones.objects.filter(ticket__cliente=request.user.id).order_by('-id')[:8]
		



	return render(request,'tickets_asignados.html', {'ticket_reasignado':ticket_reasignado,'noti':noti,'grupo':grupo,'first_name':first_name,'username':username,'ticket_cerrados':ticket_cerrados,'ticket_atendido':ticket_atendido,'ticket_nuevo':ticket_nuevo,'ticket_preatendido':ticket_preatendido})

def ver_usuario(request,id):

	usuario = User.objects.get(id=id)
	x=User.objects.get(pk=id)
	grupo =x.groups.get()
	grupo=str(grupo)
	username = request.user.username
	first_name = request.user.first_name
	return render(request,'ver_usuario.html', {'first_name':first_name,'username':username,'usuario':usuario,'grupo':grupo})



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

def logeo(request):

	return render(request, 'logeo.html', {})




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

def mticket(request,estado):

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
		ticket = Ticket.objects.filter(estado=estado,soporte_actual=username).order_by('-id')

	

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
		estado_name= 'Asignado'
	if str(estado)=='6': 
		estado_name= 'Reasignado'

	event = Evento.objects.count()



	if grupo == 'Soporte':

		noti = Notificaciones.objects.all().order_by('-id')[:8]

	if grupo == 'Clientes':

		noti = Notificaciones.objects.filter(ticket__cliente=request.user.id).order_by('-id')[:8]
		

	return render(request, 'mhome.html', {'event':event,'noti':noti,'nsoporte':nsoporte,'count':count,'soporte':soporte,'estado_name':estado_name,'tipos':tipos,'form': form,'username':username,'ticket':ticket,'grupo':grupo})



def logeate(request):
 
	return render_to_response('logeate.html', context_instance=RequestContext(request))


def logeate_m(request):
 
	return render_to_response('logeate_m.html', context_instance=RequestContext(request))

def push(request):

	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)

	x= User.objects.get(username=str(user))
	groups=x.groups.get()
	groups =str(groups)




	if user is not None:
		if user.is_active:
			login(request, user)
			if (str(username)=='root'):
				return HttpResponse(simplejson.dumps('Admin')) 


			return HttpResponse(simplejson.dumps(groups)) 
		else:
			return HttpResponse(simplejson.dumps('Desactivado')) 
	else:
		return HttpResponse(simplejson.dumps('Usuario Incorrecto'))






def salir(request):

	logout(request)

	return render_to_response('logeate.html', context_instance=RequestContext(request))


def msalir(request):

	logout(request)

	return render_to_response('logeate_m.html', context_instance=RequestContext(request))

def canvas(request):

	return render_to_response('canvas.html', context_instance=RequestContext(request))

def ver_ticket_gilda(request,ticket):

	ticket =Ticket.objects.get(id=ticket)

	return render(request, 'ver_ticket_gilda.html', {'ticket':ticket})

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
	u=ticket.cliente
	email_cliente = str(u.email)
	email_root = str(User.objects.get(id=1).email)

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
		first_name = str(ticket.cliente.first_name)

		cuerpo =  chr(10)+chr(10)+'Soporte : '+ str(soporte.soporte)+chr(10)+'Asunto : '+ str(ticket.asunto)+ chr(10) + 'Cliente : ' + str(ticket.cliente)+chr(10)+ 'Tipo : ' +str(ticket.tipo)+chr(10)+'Descripcion : '+str(ticket.descripcion)+chr(10)+'Fecha : '+str(soporte.fecha_inicio) +chr(10)

		send_mail('Xiencias Ticket Atendido '+first_name, 'El ticket fue atendido' + cuerpo, 'xienwork@sandboxbb5414fe26d94969aa76e2ece53f668e.mailgun.org', [email_cliente,email_root], fail_silently=False)


		noti=ticket.notificaciones_set.create(name='Ticket atendido -',fecha_inicio=fecha_inicio)
		noti.save()
		
		return HttpResponseRedirect("/mticket/2")

	if ticket.estado_id ==5 :

		ticket.estado_id = 2

		ticket.save()
		first_name = str(ticket.cliente.first_name)

		cuerpo =  chr(10)+chr(10)+'Ticket Atendido  : '+chr(10)+'Asunto : '+ str(ticket.asunto)+ chr(10) + 'Cliente : ' + str(ticket.cliente)+chr(10)+ 'Tipo : ' +str(ticket.tipo)+chr(10)+'Descripcion : '+str(ticket.descripcion)+chr(10)

		send_mail('Xiencias Ticket Atendido '+first_name, 'El ticket fue atendido' + cuerpo, 'xienwork@sandboxbb5414fe26d94969aa76e2ece53f668e.mailgun.org', [email_cliente,email_root], fail_silently=False)


		noti=ticket.notificaciones_set.create(name='Ticket atendido -',fecha_inicio=fecha_inicio)
		noti.save()

	if ticket.estado_id ==6 :

		ticket.estado_id = 2
		ticket.save()
		first_name = str(ticket.cliente.first_name)

		cuerpo =  chr(10)+chr(10)+'Ticket Atendido  : '+chr(10)+'Asunto : '+ str(ticket.asunto)+ chr(10) + 'Cliente : ' + str(ticket.cliente)+chr(10)+ 'Tipo : ' +str(ticket.tipo)+chr(10)+'Descripcion : '+str(ticket.descripcion)+chr(10)

		send_mail('Xiencias Ticket Atendido '+first_name, 'El ticket fue atendido' + cuerpo, 'xienwork@sandboxbb5414fe26d94969aa76e2ece53f668e.mailgun.org', [email_cliente,email_root], fail_silently=False)


		noti=ticket.notificaciones_set.create(name='Ticket atendido -',fecha_inicio=fecha_inicio)
		noti.save()


	return HttpResponseRedirect("/mdetalle_ticket/"+id+"/")

def cerrar(request,id):

	ticket= Ticket.objects.get(id=id)
	ticket.estado_id = 3
	ticket.save()

	return HttpResponseRedirect("/mticket/5")





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
	ticket_atendido= Soporte.objects.filter(ticket__estado=2).values('soporte','soporte__first_name','soporte__username','ticket__fecha_inicio','ticket_id','ticket__asunto').annotate(dcount=Max('fecha_inicio')).order_by('-id')
	ticket_preatendido= Soporte.objects.filter(ticket__estado=5).values('soporte__username','soporte__first_name','ticket__fecha_inicio','ticket_id','ticket__asunto').annotate(dcount=Max('fecha_inicio')).order_by('-id')
	ticket_cerrados= Soporte.objects.filter(ticket__estado=3).values('soporte__username','soporte__first_name','ticket__fecha_inicio','ticket_id','ticket__asunto').annotate(dcount=Max('fecha_inicio')).order_by('-id')
	ticket_reasignado= Soporte.objects.filter(ticket__estado=6,fecha_fin=None).values('ticket__cliente','soporte__username','soporte__first_name','ticket__fecha_inicio','ticket_id','ticket__asunto').annotate(dcount=Max('fecha_inicio')).order_by('-id')
	
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

	if grupo == 'Soporte':

		noti = Notificaciones.objects.all().order_by('-id')[:8]

	if grupo == 'Clientes':

		noti = Notificaciones.objects.filter(ticket__cliente=request.user.id).order_by('-id')[:8]
		

	if grupo == 'Soporte':

		return render(request,'gilda.html', {'noti':noti,'ticket_reasignado':ticket_reasignado,'ticket_cerrados':ticket_cerrados,'ticket_preatendido':ticket_preatendido,'ticket_atendido':ticket_atendido,'ticket_nuevo':ticket_nuevo,'user_soporte':user_soporte,'username':username,'grupo':grupo,'tipo':tipo})

	if grupo == 'Clientes':

		return render(request,'error.html', {'noti':noti,'ticket_reasignado':ticket_reasignado,'ticket_cerrados':ticket_cerrados,'ticket_preatendido':ticket_preatendido,'ticket_atendido':ticket_atendido,'ticket_nuevo':ticket_nuevo,'user_soporte':user_soporte,'username':username,'grupo':grupo,'tipo':tipo})


def asignar_post_gilda_new(request,soporte,ticket):

	user_soporte = User.objects.get(id=soporte)
	email = str(user_soporte.email)

	fecha_inicio = datetime.datetime.today()
	ticket = Ticket.objects.get(id=ticket)
	ticket.estado_id = 5
	ticket.soporte_actual = str(user_soporte.username)
	ticket.save()

	first_name = str(ticket.cliente.first_name)

	sa = ticket.soporte_set.create(fecha_inicio=fecha_inicio,soporte_id=soporte)
	noti=ticket.notificaciones_set.create(name='Ticket by cellphone',fecha_inicio=fecha_inicio)
	noti.save()

	cuerpo =  chr(10)+chr(10)+'Soporte asignado  : '+ str(sa.soporte)+chr(10)+'Ticket'+chr(10)+'Asunto : '+ str(ticket.asunto)+ chr(10) + 'Cliente : ' + str(ticket.cliente)+chr(10)+ 'Tipo : ' +str(ticket.tipo)+chr(10)+'Descripcion : '+str(ticket.descripcion)+chr(10)+'Fecha : '+str(sa.fecha_inicio) +chr(10)

	send_mail('Xiencias Ticket Asignado '+first_name, 'El ticket fue asignado' + cuerpo, 'xienwork@sandboxbb5414fe26d94969aa76e2ece53f668e.mailgun.org', [email], fail_silently=False)

	return HttpResponseRedirect("/gilda")




def reasignar_post_gilda_new(request,soporte_act,ticket,soporte):



	sa = Soporte.objects.get(id=soporte_act)
	print sa
	
	sa.fecha_fin = datetime.datetime.today()
	sa.soporte_id = soporte

	sa.save()

	user =User.objects.get(username=sa.soporte)
	email=str(user.email)
	print email

	user_soporte = User.objects.get(id=soporte)
	

	fecha_inicio = datetime.datetime.today()

	ticket = Ticket.objects.get(id=ticket)
	ticket.estado_id = 5
	ticket.soporte_actual = str(user_soporte.username)
	ticket.save()

	first_name = str(ticket.cliente.first_name)

	cuerpo =  chr(10)+chr(10)+'Soporte reasignado  : '+ str(sa.soporte)+chr(10)+'Ticket'+chr(10)+'Asunto : '+ str(ticket.asunto)+ chr(10) + 'Cliente : ' + str(ticket.cliente)+chr(10)+ 'Tipo : ' +str(ticket.tipo)+chr(10)+'Descripcion : '+str(ticket.descripcion)+chr(10)+'Fecha : '+str(sa.fecha_inicio) +chr(10)

	send_mail('Xiencias Ticket Reasignado '+first_name, 'El ticket fue reasignado' + cuerpo, 'xienwork@sandboxbb5414fe26d94969aa76e2ece53f668e.mailgun.org', [email], fail_silently=False)


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
		first_name = str(ticket.cliente)

		id = request.POST['id']
		fecha_inicio = datetime.datetime.today()
		soporte = Soporte.objects.get(id=id)
		fecha_fin = datetime.datetime.today()
		soporte.fecha_fin = fecha_fin

		soporte.save()



		soporte_r= ticket.soporte_set.create(fecha_inicio=fecha_fin,soporte_id=soporte_user)

		ticket.soporte_actual = str(soporte_r.soporte)
		ticket.save()

		cuerpo =  chr(10)+chr(10)+'Soporte reasignado  : '+ str(soporte_r.soporte)+chr(10)+'Ticket'+chr(10)+'Asunto : '+ str(ticket.asunto)+ chr(10) + 'Cliente : ' + str(username)+chr(10)+ 'Tipo : ' +str(ticket.tipo)+chr(10)+'Descripcion : '+str(ticket.descripcion)+chr(10)+'Fecha : '+str(soporte.fecha_inicio) +chr(10)

		send_mail('Xiencias Ticket Reasignado '+first_name, 'El ticket fue reasignado' + cuerpo, 'xienwork@sandboxbb5414fe26d94969aa76e2ece53f668e.mailgun.org', ['joelunmsm@gmail.com'], fail_silently=False)

		noti=ticket.notificaciones_set.create(name='Ticket reasignado ',fecha_inicio=fecha_inicio)
		
		noti.save()

		return HttpResponseRedirect("/mdetalle_ticket/"+id_ticket+"/")



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
	username = request.user.username
	first_name = str(ticket.cliente.first_name)
	x=User.objects.get(username=username)
	grupo =x.groups.get()
	grupo= str(grupo)
	
	ticket.save()

	user = User.objects.get(username=ticket.cliente)

	if user.username == username :
		if ticket.soporte_actual != '' :
			email= User.objects.get(username=ticket.soporte_actual).email
		else:
			email='xiencias@gmail.com'
	else:
		email= User.objects.get(username=ticket.cliente).email

	if ticket.soporte_actual != '' :

		soporte = Soporte.objects.get(soporte__username=ticket.soporte_actual,ticket=id)
		soporte.fecha_fin = fecha_fin
		soporte.save()



	ta = Ticket.objects.filter(estado_id=5)
	ta=ta.count()


	cuerpo =  chr(10)+chr(10)+'Ticket : '+ str(ticket.asunto)+chr(10)+'Fecha Cierre: '+str(ticket.fecha_fin)+chr(10)+'Fecha Inicio: '+str(ticket.fecha_inicio)+chr(10)+'Soporte Actual: '+ str(ticket.soporte_actual)


	send_mail('Xiencias Ticket Cerrado '+first_name, 'El ticket fue cerrado' + cuerpo, 'xienwork@sandboxbb5414fe26d94969aa76e2ece53f668e.mailgun.org', [str(email)], fail_silently=False)

	if grupo =='Soporte':

		if (ta==0):

			return HttpResponseRedirect("/mticket/5")

		else:

			return HttpResponseRedirect("/mticket/6")
	else:

		return HttpResponseRedirect("/mticket/3")




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

def mdetalle_ticket(request,id):

	ticket= Ticket.objects.get(id=id)
	soportes = ticket.soporte_set.all()

	id = request.user.id
	user = User.objects.get(id=id)
	username = request.user.username
	
	tipos=Tipo.objects.all()
	x=User.objects.get(username=username)
	grupo =x.groups.get()
	grupo= str(grupo)
	estado= str(ticket.estado)

	fit=ticket.fecha_inicio
	today = datetime.datetime.today()

	x=str(today-fit)
	espera=x.split('.')[0]


	if grupo == 'Soporte':

		noti = Notificaciones.objects.all().order_by('-id')[:8]

	if grupo == 'Clientes':

		noti = Notificaciones.objects.filter(ticket__cliente=request.user.id).order_by('-id')[:8]
		
	
	event = Evento.objects.count()

	return render(request, 'mdetalle_ticket.html', {'user':user,'espera':espera,'estado':estado,'event':event,'noti':noti,'soportes':soportes,'username':username,'grupo':grupo,'tipos':tipos,'ticket':ticket})



def evento(request,id,id_ticket):

	soporte = Soporte.objects.get(id=id)
	ticket = Ticket.objects.get(id=id_ticket)
	#soporte.evento_set.create(fecha_inicio=fecha_inicio,name=name)
	username = request.user.username
	x=User.objects.get(username=username)
	grupo =x.groups.get()
	grupo= str(grupo)

	return render(request, 'evento_add.html', {'ticket':ticket,'soporte':soporte,'grupo':grupo})

def soportes(request,id):

	ticket= Ticket.objects.get(id=id)
	soportes = ticket.soporte_set.all()


	return render(request, 'soportes.html', {'ticket':ticket,'soportes':soportes})

def soporte(request,id):


	soporte= Soporte.objects.get(id=id)

	return render(request, 'soporte.html', {'soporte':soporte})


def eventos(request,id):

	soporte= Soporte.objects.get(id=id)
	eventos = soporte.evento_set.all()
	username = request.user.username

	x=User.objects.get(username=username)
	grupo =x.groups.get()
	grupo= str(grupo)



	return render(request, 'eventos.html', {'soporte':ticket,'eventos':eventos,'grupo':grupo})



def evento_add(request):

	
	if request.method == 'POST':

		evento_id = request.POST['id_ticket']
		soporte_id = request.POST['id']
		user = 	request.user.id	
		email1 = request.user.email
		username = 	request.user.username
		first_name	= request.user.first_name
		name = request.POST['name']
		fecha_inicio = datetime.datetime.today()
		c=Ticket.objects.get(id=evento_id)

		name =str(c.cliente.first_name)

	
		email2 =str(c.cliente.email)

		if (email1 == email2):

			s=c.soporte_set.order_by('-id')[:1].get()
			u=s.soporte
			email = u.email
		
		else:

			email = email2

		print email


		ix = request.POST['cont']		

		doc= chr(10)

		for i in range (1, int(ix)+1):
		
			newdoc = Document(docfile = request.FILES['docfile'+str(i)],ticket_id=evento_id,user_id=user)
			newdoc.save()

			doc = doc + 'http://www.xiencias.org/html/'+str(newdoc.docfile)+chr(10)


		soporte = Soporte.objects.get(id=soporte_id)

		evento=soporte.evento_set.create(fecha_inicio=fecha_inicio,name=name,user_id=user)

		cuerpo =  chr(10)+chr(10)+'Evento : '+ str(evento.name)+chr(10)+'Ticket'+chr(10)+'Asunto : '+ str(c.asunto)+ chr(10) + 'Cliente : ' + str(username)+chr(10)+ 'Tipo : ' +str(c.tipo)+chr(10)+'Descripcion : '+str(c.descripcion)+chr(10)+'Fecha : '+str(evento.fecha_inicio) +chr(10)+'Archivos adjuntos : ' + doc

		send_mail('Xiencias Ticket Evento '+first_name, 'Se agrego un nuevo evento por ' +str(name)+ cuerpo, 'xienwork@sandboxbb5414fe26d94969aa76e2ece53f668e.mailgun.org', [email], fail_silently=False)


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

		tipo = Tipo.objects.get(id=tipo)
		tipo=str(tipo.name)
		descripcion=request.POST['descripcion']

		fecha_inicio = datetime.datetime.today()



		print fecha_inicio
		#estado 1=Nuevo	2=Atendido 3=Prueba 4=Cerrado
		#tipo 1=Incidencia 2=Requerimento

		c=User.objects.get(pk=id).ticket_set.create(cliente=username,asunto=asunto,tipo_id=1,descripcion=descripcion,fecha_inicio=fecha_inicio,estado_id=1)
		
		c.save()	

		first_name =str(c.cliente.first_name)
		
		noti=c.notificaciones_set.create(name='Ticket nuevo ',fecha_inicio=fecha_inicio)
		
		noti.save()

		ix = request.POST['cont']

		doc=chr(10)		

		for i in range (1, int(ix)+1):
		
		
			newdoc = Document(docfile = request.FILES['docfile'+str(i)],ticket_id=c.id,user_id=id)
			newdoc.save()

			doc = doc + 'http://www.xiencias.org/html/'+str(newdoc.docfile)+chr(10)

		s= str(fecha_inicio)

		fecha_inicio=str(s.split('.')[0])
		

		cuerpo =  chr(10)+chr(10)+'Asunto : '+ str(asunto)+ chr(10) + 'Generado por : ' + str(username)+chr(10)+ 'Tipo : ' +str(tipo)+chr(10)+'Descripcion : '+str(descripcion)+chr(10)+'Fecha : '+str(fecha_inicio)+chr(10)+'Archivos adjuntos : ' + doc 

		send_mail('Xiencias Ticket Nuevo '+first_name, 'Se agrego un ticket' + cuerpo, 'xienwork@sandboxbb5414fe26d94969aa76e2ece53f668e.mailgun.org', ['joelunmsm@gmail.com','xiencias@gmail.com'], fail_silently=False)

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


def agregar_ticket_movil(request):
    # Handle file upload
	
	username = request.user.username

	if request.method == 'POST':

		id = request.user.id
		form = DocumentForm(request.POST, request.FILES)

		username = request.user.username
		first_name = str(request.user.first_name)

		asunto = request.POST['asunto']
		tipo = request.POST['tipo']

		tipo = Tipo.objects.get(id=tipo)
		tipo=str(tipo.name)
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

		doc=chr(10)		

		for i in range (1, int(ix)+1):
		
		
			newdoc = Document(docfile = request.FILES['docfile'+str(i)],ticket_id=c.id,user_id=id)
			newdoc.save()

			doc = doc + 'http://www.xiencias.org/html/'+str(newdoc.docfile)+chr(10)


		cuerpo =  chr(10)+chr(10)+'Asunto : '+ str(asunto)+ chr(10) + 'Generado por : ' + str(username)+chr(10)+ 'Tipo : ' +str(tipo)+chr(10)+'Descripcion : '+str(descripcion)+chr(10)+'Fecha : '+str(fecha_inicio)+chr(10)+'Archivos adjuntos : ' + doc 

		send_mail('Xiencias Ticket Nuevo '+first_name, 'Se agrego un ticket' + cuerpo, 'xienwork@sandboxbb5414fe26d94969aa76e2ece53f668e.mailgun.org', ['joelunmsm@gmail.com','xiencias@gmail.com'], fail_silently=False)

		# Redirect to the document list after POST
		
		return render_to_response(
        'movil.html',
        {},
        context_instance=RequestContext(request)
    )
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

	return render(request, 'documentos.html', {'documentos':documentos,'grupo':grupo,'noti':noti,'username':username,'ticket':ticket})


def list1(request):

	if request.method == 'POST':

		id = request.user.id
		form = DocumentForm(request.POST, request.FILES)
		ticket = request.POST['ticket']
		print ticket
		username = request.user.username
		first_name = str(request.user.first_name)
		c= Ticket.objects.get(id=ticket)

		fecha_inicio = datetime.datetime.today()
		#estado 1=Nuevo	2=Atendido 3=Prueba 4=Cerrado 5 =Preatendido 
		#tipo 1=Incidencia 2=Requerimento


		noti=c.notificaciones_set.create(name='Archivo nuevo ',fecha_inicio=fecha_inicio)
		noti.save()

		ix = request.POST['cont']
			

		doc= chr(10)

		for i in range (1, int(ix)+1):
		
			newdoc = Document(docfile = request.FILES['docfile'+str(i)],ticket_id=c.id,user_id=id)
			newdoc.save()

			doc = doc + 'http://www.xiencias.org/html/'+str(newdoc.docfile)+chr(10)


		cuerpo =  chr(10)+chr(10)+'Archivos adjuntos : ' + doc+chr(10)+'Asunto : '+ str(c.asunto)+ chr(10) + 'Cliente : ' + str(username)+chr(10)+ 'Tipo : ' +str(c.tipo)+chr(10)+'Descripcion : '+str(c.descripcion)+chr(10)+'Fecha : '+str(c.fecha_inicio) 

		send_mail('Xiencias Ticket Document '+first_name, 'Se agrego un nuevo documento adjunto' + cuerpo, 'xienwork@sandboxbb5414fe26d94969aa76e2ece53f668e.mailgun.org', ['joelunmsm@gmail.com','xiencias@gmail.com'], fail_silently=False)


		
            # Redirect to the document list after POST
		return HttpResponseRedirect("/documentos/"+str(ticket))

def agregar_ticket_m(request):

	tipos=Tipo.objects.all()
	username = request.user.username

	x=User.objects.get(username=username)
	grupo =x.groups.get()
	grupo= str(grupo)


	return render(request, 'agregar_ticket_m.html', {'tipos':tipos,'username':username,'grupo':grupo})

def agregarm(request,a,b):

	tipos=Tipo.objects.all()
	
	return render(request,'am.html', {'tipos':tipos})


def arduino(request):

	
	
	return render(request,'web/arduino.html', {})
	
