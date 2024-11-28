from django.db import models
from Usuarios.models import CustomUser

# Create your models here.
class Rubro(models.Model):
    nombre = models.CharField(max_length=50)
    imagen = models.ImageField(null=True, blank=True, upload_to='images/', default='images/sin_Imagen.png')

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    imagen_1 = models.ImageField(null=True, blank=True, upload_to='images/', default='images/sin_Imagen.png')
    imagen_2 = models.ImageField(null=True, blank=True, upload_to='images/', default='images/sin_Imagen.png')
    imagen_3 = models.ImageField(null=True, blank=True, upload_to='images/', default='images/sin_Imagen.png')
    
    
    def __str__(self):
        return self.nombre

ELECCION_ESTADO=[
    (1,'Muy bueno'),
    (2,'Bueno'),
    (3,'Regular'),
    (4,'Reparar')
]

ELECCION_VIGENCIA=[
    (1,'VIGENTE'),
    (2,'ELIMINADO'),
    (3,'SUSPENDIDO')
]

class Publicacion(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=200)
    valor = models.DecimalField(decimal_places=2,max_digits=9)
    estado=models.IntegerField(choices=ELECCION_ESTADO,default=1,null=False,blank=False)
    descuento = models.IntegerField(null=True,blank=True)
    vigencia = models.IntegerField(choices=ELECCION_VIGENCIA,default=1,null=False,blank=False)
    rubro = models.ForeignKey(Rubro, on_delete=models.CASCADE,null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comentarios = models.IntegerField(default=0, null=False,blank=False)

    def __str__(self):
        return self.nombre