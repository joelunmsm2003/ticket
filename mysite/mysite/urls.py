from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic import RedirectView
admin.autodiscover()

urlpatterns = patterns('',

	url(r'^admin/', include(admin.site.urls)),
 	url(r'^logeate/', 'ticket.views.logeate', name='reporte'),

	url(r'^push$', 'ticket.views.push'),
	url(r'^ticket/(\d+)/$', 'ticket.views.ticket'),
	url(r'^salir/', 'ticket.views.salir'),
	url(r'^cerrar/(\d+)/$', 'ticket.views.cerrar'),
	url(r'^validar/(\d+)/$', 'ticket.views.validar'),
	url(r'^editar_ticket/(\d+)/$','ticket.views.editar_ticket'),
	url(r'^reasignar_add/', 'ticket.views.reasignar_add'),
	url(r'^atender/(\d+)/$','ticket.views.atender'),
	url(r'^evento_add/(\d+)/$','ticket.views.evento_add'),
	url(r'^reasignar/(\d+)/(\d+)/$','ticket.views.reasignar'),
	url(r'^ver_ticket/(\d+)/$','ticket.views.ver_ticket'),
	url(r'^realtime_post$', 'ticket.views.realtime_post'),
	url(r'^realtime_post_monitor$', 'ticket.views.realtime_post_monitor'),
	url(r'^detalle_ticket/(\d+)/$','ticket.views.detalle_ticket'),
	url(r'^evento/(\d+)/(\d+)/$', 'ticket.views.evento'),
	url(r'^evento_add/', 'ticket.views.evento_add'),
	url(r'^ver_evento/(\d+)/(\d+)/$', 'ticket.views.ver_evento'),
	url(r'^realtime/$', 'ticket.views.realtime'),
	url(r'^ver_usuario/(\d+)/$', 'ticket.views.ver_usuario'),
	url(r'^notificaciones/$', 'ticket.views.notificaciones'),
	url(r'^agregar_ticket/$', 'ticket.views.agregar_ticket', name='agregar_ticket'),
	url(r'^list1/$', 'ticket.views.list1', name='list1'),
	url(r'^documentos/(\d+)/$', 'ticket.views.documentos'),
	url(r'^asignar_gilda/(\d+)/$','ticket.views.asignar_gilda'),
	url(r'^gilda/$','ticket.views.gilda'),
	
	url(r'^reasignar_gilda/(\d+)/$','ticket.views.reasignar_gilda'),
	
	url(r'^reasignar_post_gilda_new/(\d+)/(\d+)/(\d+)/$', 'ticket.views.reasignar_post_gilda_new'),
	url(r'^asignar_post_gilda_new/(\d+)/(\d+)/$', 'ticket.views.asignar_post_gilda_new'),
	url(r'^tickets_asignados/', 'ticket.views.tickets_asignados'),
)


