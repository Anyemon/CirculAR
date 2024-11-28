from django.shortcuts import get_object_or_404,render, redirect
from django.template import TemplateDoesNotExist
from .models import Publicacion, Compra, Trueque
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.conf import settings
from django.urls import reverse
from .forms import CompraForm, TruequeForm
from inbox.views import notificacion




@login_required
def realizar_compra(request, id):
    # Obtén la publicación con el id dado

    publicacion = Publicacion.objects.get (id=id)
    if publicacion.usuario == request.user:
       
        messages.error(request, 'No puedes comprar tu propia publicación.')
        return redirect('publicacion:lista_publicaciones')  
    if request.method == 'POST':
        medio_pago = request.POST.get('medio_pago')
        
        # Redirigir según el medio de pago seleccionado
        if medio_pago == 'EFECTIVO':
           return redirect('compra:pago_efectivo', publicacion_id=publicacion.id)
        elif medio_pago == 'TRANSFERENCIA':
            return redirect('compra:pago_transferencia', publicacion_id=publicacion.id)
        elif medio_pago == 'MERCADOPAGO':
            #return redirect('crear_preferencia', publicacion_id=publicacion.id)
            return redirect('api:procesar_pago', publicacion_id=publicacion.id)
        elif medio_pago == 'TRUEQUE':
            return redirect('compra:trueque', publicacion_id=publicacion.id)
        
        publicacion.vigencia=3  # Establecer a 'SUSPENDIDO'
        publicacion.save()
        return redirect('compra:compras_realizadas')  
    
    return render(request, 'realizar_compra.html', {'publicacion': publicacion})

@login_required
def pago_efectivo(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)

    if request.method == 'POST':
        # Crear y guardar la compra en la base de datos
        compra = Compra(
            publicacion=publicacion,
            usuario=request.user,
            medio_pago='efectivo'
        )
        compra.save()
        pago_confirmado = True  # Cambia esta condición según tu lógica de pago

        if pago_confirmado:
            publicacion.vigencia = 3  # Establecer a 'SUSPENDIDO'
            publicacion.save()
            messages.success(request, 'Compra realizada con éxito.')
            return redirect('compra:compras_realizadas')
        else:
            messages.error(request, 'El pago no pudo ser procesado.')
            return redirect('publicacion:lista_publicaciones')

    return render(request, 'pago_efectivo.html', {'publicacion': publicacion})


def compras_realizadas(request):
    #lista_compra = Compra.objects.filter(usuario=request.user,).order_by('-id')
    #lista_compra = Compra.objects.all().order_by('-id').filter(usuario=request.user.id)
    #lista_compra = Compra.objects.filter(usuario=request.user).order_by('-id')
    lista_compra = Compra.objects.filter(usuario=request.user).order_by('-id')
    print(lista_compra)

    context = {
        'compras_realizadas': lista_compra
    }
    #return redirect(reverse('compras_realizadas', args=[publicacion_id]))
    return render(request, 'compras_realizadas.html', context)

@login_required
def pago_transferencia(request, publicacion_id): 
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    
    if request.method == 'POST':
        form = CompraForm(request.POST, request.FILES)
        if form.is_valid():
            # Guarda el formulario y la información del comprobante
            compra = form.save(commit=False)
            compra.publicacion = publicacion
            compra.usuario = request.user
            compra.metodo_pago = 'transferencia'
            compra.save()
            pago_confirmado = True  # Cambia esta condición según tu lógica

        if pago_confirmado:
            publicacion.vigencia = 3  # Establecer a 'SUSPENDIDO'
            publicacion.save()
            messages.success(request, 'Compra realizada con éxito.')
        return redirect('compra:compras_realizadas')
    else:
        form = CompraForm()  # Esta línea asegura que 'form' se defina siempre, incluso si no es POST.
    
    return render(request, 'pago_transferencia.html', {
        'publicacion': publicacion,
        'form': form
    })


def trueque_view(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    
    if request.method == 'POST':
        trueque = request.POST.get('producto')
        
        # Redirigir según el medio de pago seleccionado
        if trueque == 'publicado':
           return redirect('compra:publicado', publicacion_id=publicacion.id)
        elif trueque == 'nuevoproducto':
            return redirect('compra:nuevo_producto', publicacion_id=publicacion.id)
       
      
        publicacion.vigencia=3  # Establecer a 'SUSPENDIDO'
        publicacion.save()
        return redirect('compra:trueque_realizado')  
    
    return render(request, 'trueque.html', {'publicacion': publicacion})

def publicado(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    
    # Obtener las publicaciones disponibles para trueque que no están vendidas (estado != 'vendida')
    lista_publicaciones = Publicacion.objects.filter(usuario=request.user, vigencia=1)
    #lista_publicaciones = Publicacion.objects.filter(usuario=request.user).exclude(estado=3)  # estado '1' es el estado disponible
   
    
    if request.method == 'POST':
        # Verificar si el usuario ha seleccionado una publicación
        publicacion_seleccionada_id = request.POST.get('publicacion_seleccionada_id')

        if publicacion_seleccionada_id:
            # Verificar que la publicación seleccionada esté en estado '1' (disponible para trueque)
            publicacion_seleccionada = get_object_or_404(Publicacion, id=publicacion_seleccionada_id)

            # Crear el trueque
            trueque = Trueque(usuario=request.user, publicacion=publicacion)
            trueque.producto_ofrecido = publicacion_seleccionada.nombre  # Asocia el nombre de la publicación
            trueque.producto = publicacion_seleccionada.producto
            trueque.save()

            trueque_confirmado = True

            if trueque_confirmado:
                publicacion.vigencia = 3  # Establecer a 'SUSPENDIDO'
                publicacion.save()


            # Notificación y mensaje de éxito
            notificacion(request, publicacion, 3)
            messages.success(request, 'Has ofrecido tu producto para el trueque exitosamente.')
            return redirect('compra:trueque_realizado')

        else:
            messages.error(request, "Debe seleccionar una publicación válida para el trueque.")
    
    return render(request, 'publicado.html', {
        'publicacion_id': publicacion_id,
        'lista_publicaciones': lista_publicaciones
    })
@login_required
def ofrecer_trueque(request, publicacion_id,):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    # Lógica para crear el trueque
    trueque = Trueque.objects.create(
        publicacion=publicacion,
        usuario=request.user,
        estado_trueque='pendiente'
    )
    messages.success(request, '¡Has ofrecido el trueque con éxito!')

    # Redirigir a la vista de trueque_realizado
    return redirect('compra:trueque_realizado')

def nuevo_producto(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)

    if request.method == 'POST':
        form = TruequeForm(request.POST, request.FILES)
        if form.is_valid():
            
            trueque = form.save(commit=False)
            trueque.usuario = request.user  # Asocia el usuario actual
            
            trueque.publicacion = publicacion  # Asocia la publicación correspondiente
            trueque.save()

            trueque_aprobado = True

            if trueque_aprobado:
                publicacion.vigencia = 3  # Establecer a 'SUSPENDIDO'
            trueque_rechazado = False
            if trueque_rechazado:
                publicacion.vigencia = 1
                publicacion.save()
                
            notificacion(request,publicacion,3)
            messages.success(request, 'Has ofrecido tu producto para el trueque exitosamente. El vendedor responderá a la brevedad.')
            return redirect('compra:trueque_realizado')

    else:
        form = TruequeForm()

    return render(request, 'nuevo_producto.html', {'form': form, 'publicacion_id': publicacion_id})
   
@login_required
def trueque_realizado(request):
    # Trueques donde el usuario es quien hizo la oferta (ofrecidos)
    trueques_ofrecidos = Trueque.objects.filter(usuario=request.user).order_by('-id')
 
    # Trueques donde el usuario es el dueño de la publicación (recibidos)
    trueques_recibidos = Trueque.objects.filter(publicacion__usuario=request.user).order_by('-id')
   
    context = {
        'trueques_ofrecidos': trueques_ofrecidos,
        'trueques_recibidos': trueques_recibidos,
    }
    
    return render(request, 'trueque_realizado.html', context)