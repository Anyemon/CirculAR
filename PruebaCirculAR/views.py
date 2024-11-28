from django.shortcuts import render
from publicacion.models import Publicacion, Rubro 
from inbox.models import Conversacion

def home(request):
    rubro = Rubro.objects.all()[:4]
    lista_prod_rand = Publicacion.objects.all().filter(vigencia=1).order_by('?')[:4]
    lista_prod_last = Publicacion.objects.all().filter(vigencia=1).order_by('-id')[:4]
    if request.method=='GET':
        usuario=request.user
        notificacion=False
        if usuario.is_authenticated:
            for conversacion in Conversacion.objects.filter(participantes=request.user):
                ultimo_mensaje=conversacion.mensajes.last()
                if (conversacion.fue_visto == False) and (ultimo_mensaje.remitente != request.user):
                    notificacion=True
    context={
            'usuario':usuario,
            'lista_prod_rand': lista_prod_rand, 
            'lista_prod_last':lista_prod_last,
            'notificacion':notificacion,
            'rubro': rubro
            }
    return render(request,'home.html',context)
##aversers


def acerca(request):
    return render(request, 'footer_info.html')

def faq(request):
    return render(request, 'footer_info.html')

def terminos(request):
    return render(request, 'footer_info.html')

def privacidad(request):
    return render(request, 'footer_info.html')
