from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    direccion = models.CharField(max_length=200,default='')
    altura = models.SmallIntegerField(default=0)
    fechaDeNacimiento = models.DateField(null=True)
    estado = models.CharField(max_length=1,default='V')
    avatar = models.ImageField(null=True, blank=True, upload_to='images/', default='images/sin_avatar.png')

class Black_list(models.Model):
    login = models.CharField(max_length=50)
    estado = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.nombre