from django.db import models
from Usuarios.models import CustomUser
from publicacion.models import Publicacion, Producto
from django.conf import settings


MEDIO_PAGO_CHOICES = [
    ('EFECTIVO', 'pago_efectivo'),
    ('TRANSFERENCIA', 'pago_transferencia'),
    ('MERCADOPAGO', 'api:procesar_pago'),
    ('TRUEQUE', 'trueque'),
]

class Compra(models.Model):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE,null=True)
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)
    numeroComprobante = models.CharField(max_length=255, blank=True, null=True)
    imagen = models.ImageField(upload_to='comprobantes/', blank=True, null=True)
    fechaDeTransferencia = models.DateField(blank=True, null=True)
    fecha_compra = models.DateTimeField(auto_now_add=True, null=True)
    medio_pago = models.CharField(max_length=20, choices=MEDIO_PAGO_CHOICES)

    def __str__(self):
        return f"Compra {self.id} realizada el {self.fecha_compra}"

    
class Trueque(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE,null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)
    producto_ofrecido = models.TextField()
    imagen1 = models.ImageField(upload_to='trueque_images/', null=True, blank=True)
    imagen2 = models.ImageField(upload_to='trueque_images/', null=True, blank=True)

    vendedor_respondio = models.BooleanField(default=False)

    respuesta_vendedor = models.TextField(blank=True, null=True)  # Campo para contraoferta o mensaje de respuesta
    estado_trueque = models.CharField(max_length=10,choices=[('pendiente', 'Pendiente'), ('aceptado', 'Aceptado'), ('rechazado', 'Rechazado')],default='pendiente')

    def __str__(self):
        return self.producto_ofrecido