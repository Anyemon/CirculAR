import mercadopago
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from .models import Publicacion 
from .models import Venta
from django.contrib import messages
from django.contrib.auth.decorators import login_required



def procesar_pago(request, publicacion_id):
   
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)



    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

    preference_data = {
        "items": [
            {
                "title": publicacion.nombre,
                "quantity": 1,
                "currency_id": "ARS",
                "unit_price": float(publicacion.valor)
            }
        ],
        "back_urls": {
              "success": f"http://127.0.0.1:8000/pago_exitoso/?publicacion_id={publicacion.id}",
            "failure": "http://127.0.0.1:8000/pago_fallido/",
            "pending": "http://127.0.0.1:8000/pago_pendiente/"
        },
        "auto_return": "approved",
    }

    try:
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]
        return redirect(preference["init_point"])
    except Exception as e:
        print(f"Error al crear la preferencia: {str(e)}")
        return JsonResponse({'error': 'No se pudo crear la preferencia de pago.'}, status=500)
   # preference_response = sdk.preference().create(preference_data)
    #preference = preference_response["response"]

    # Redirigir al usuario a MercadoPago para completar el pago
   # return redirect(preference["init_point"])

@login_required
def pago_exitoso(request):
    publicacion_id = request.GET.get('publicacion_id')  # Obtener la publicación por ID
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)

    # Cambiar el estado de la publicación a 'SUSPENDIDO' (vigencia = 3)
    publicacion.vigencia = 3
    publicacion.save()

    # Registrar la venta en la base de datos
    venta = Venta.objects.create(
    usuario=request.user,
    publicacion=publicacion,
        
    )

    messages.success(request, 'Pago exitoso. La publicación ha sido suspendida y la venta registrada.')

    # Redirigir a la lista de "compras realizadas"
    return redirect('compra:compras_realizadas')

def pago_fallido(request):
    return render(request, 'pago_fallido.html')

def pago_pendiente(request):
    return render(request, 'pago_pendiente.html')
