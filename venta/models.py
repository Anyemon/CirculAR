from django.conf import settings 
from django.db import models
#from django.contrib.auth.models import User
from Usuarios.models import CustomUser
from publicacion.models import Publicacion, Producto
from compra.models import Trueque

class Venta(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE,null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.publicacion.nombre} vendido por {self.usuario.username} el {self.fecha}"
