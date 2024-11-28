from django.db import models
#from django.contrib.auth.models import User
from Usuarios.models import CustomUser
from django.utils import timezone
from django.utils.timesince import timesince
import uuid

# Create your models here.
class MensajeInbox(models.Model):
    remitente = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="mensaje_enviado")
    conversacion = models.ForeignKey('Conversacion', on_delete=models.CASCADE, related_name="mensajes")
    cuerpo = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['creado']
        
    def __str__(self):
        tiempo_desde = timesince(self.creado, timezone.now())
        return f'[{self.remitente.username} : {tiempo_desde} del mensaje]'

class Conversacion(models.Model):
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    participantes = models.ManyToManyField(CustomUser, related_name='conversacion')
    ultimo_mensaje_creado = models.DateTimeField(default=timezone.now)
    fue_visto = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['ultimo_mensaje_creado']
        
    def __str__(self):
        nombres_usuarios = ", ".join(user.username for user in self.participantes.all())
        return f'[{nombres_usuarios}]'
