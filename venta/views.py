from django.shortcuts import get_object_or_404, redirect, render
from .models import Venta, Publicacion,Trueque
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RespuestaTruequeForm
from inbox.views import notificacion  


def lista_ventas(request):
    # Filtrar las ventas realizadas por el usuario actual
    ventas = Venta.objects.filter(usuario=request.user)
    return render(request, 'ventas_realizadas.html', {'ventas': ventas})

@login_required
def ventas_realizadas(request):

    ventas_realizadas = Publicacion.objects.filter(usuario=request.user, vigencia=3)
    
    context = {
        'ventas_realizadas': ventas_realizadas
    }
    return render(request, 'ventas_realizadas.html', context)


@login_required
def responder_trueque(request, trueque_id, accion,):
    trueque = get_object_or_404(Trueque, id=trueque_id, publicacion__usuario=request.user)


    if accion == 'aceptado':
        trueque.estado_trueque = 'aceptado'
        trueque.save()
        trueque.respuesta_vendedor = 'Tu oferta ha sido aceptada.'
        messages.success(request, 'Has aceptado el trueque.')
        notificacion(request, trueque, 4)

    elif accion == 'rechazado':
        trueque.estado_trueque = 'rechazado'
        trueque.save()
        publicacion = trueque.publicacion
        publicacion.vigencia = 1
        publicacion.save()
        trueque.respuesta_vendedor = 'Tu oferta ha sido rechazada.'
        messages.success(request, 'Has rechazado el trueque.')
        notificacion(request, trueque, 5)

 
    trueque.save()

    return redirect('compra:trueque_realizado')
