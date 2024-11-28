from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Conversacion, MensajeInbox
from.forms import NuevoMensajeInboxForm
from django.utils import timezone

# Create your views here.
@login_required
def inbox(request,conversacion_id=None):
    mis_conversaciones = Conversacion.objects.filter(participantes=request.user)
    nuevo_mensaje_form=NuevoMensajeInboxForm()
    ultimo_mensaje=None
    notificacion=None
    identificador=None
    if conversacion_id:
        conversacion = get_object_or_404(Conversacion,id=conversacion_id)
        if request.method=='POST':
            form=NuevoMensajeInboxForm(request.POST)
            if form.is_valid():
                mensaje=form.save(commit=False)
                mensaje.remitente=request.user
                mensaje.conversacion=conversacion
                mensaje.save()
                conversacion.ultimo_mensaje_creado=timezone.now()
                conversacion.fue_visto=False
                conversacion.save()
        else:
            ultimo_mensaje=conversacion.mensajes.last()
            if (conversacion.fue_visto == False) and (ultimo_mensaje.remitente != request.user):
                conversacion.fue_visto=True
                conversacion.save()
                notificacion=False
                identificador=conversacion.id
            else:
                for conversacion in mis_conversaciones:
                    ultimo_mensaje=conversacion.mensajes.last()
                    if (conversacion.fue_visto == False) and (ultimo_mensaje.remitente != request.user) and (conversacion.id != conversacion_id):
                        notificacion=True
                        identificador=conversacion.id
            conversacion = get_object_or_404(Conversacion,id=conversacion_id)
    else:
        for conversacion in mis_conversaciones:
            ultimo_mensaje=conversacion.mensajes.last()
            if (conversacion.fue_visto == False) and (ultimo_mensaje.remitente != request.user):
                notificacion=True
                identificador=conversacion.id
        conversacion = None
        ultimo_mensaje = None
    context = {
        'conversacion':conversacion,
        'mis_conversaciones':mis_conversaciones,
        'nuevo_mensaje_form':nuevo_mensaje_form,
        'ultimo_mensaje':ultimo_mensaje,
        'notificacion':notificacion,
        'identificador':identificador
    }
    return render(request,'inbox.html',context)

def notificacion(request,publicacion,tipo_mensaje):
    id_destinatario=publicacion.usuario.pk
    conversaciones = Conversacion.objects.filter(participantes=id_destinatario)
    try:
        conversacion=get_object_or_404(conversaciones,participantes=request.user)
    except:
        conversacion=None    
    
    if conversacion:
        conversacion.ultimo_mensaje_creado=timezone.now()
        conversacion.fue_visto=False
        conversacion.save()
    else:
        conversacion=Conversacion()
        conversacion.save()
        conversacion.participantes.add(request.user)
        conversacion.participantes.add(id_destinatario)
        conversacion.save()
    mensaje=MensajeInbox()
    mensaje.conversacion=conversacion
    mensaje.remitente=request.user
    if tipo_mensaje == 1:
        mensaje.cuerpo=f"Hola, realicé una consulta en la publicación {publicacion.nombre}"
    elif tipo_mensaje == 2:
        mensaje.cuerpo=f"Hola, realicé compra de la publicación {publicacion.nombre}"
    elif tipo_mensaje == 3:
        mensaje.cuerpo=f"Hola, propuse un trueque a la publicación {publicacion.nombre}"
    elif tipo_mensaje == 4:
        mensaje.cuerpo=f"Hola, acepto el trueque. ¡Trato Hecho! "
    elif tipo_mensaje == 5:
        mensaje.cuerpo=f"Hola, no acepto el trueque. Lo lamento "
    mensaje.save()

