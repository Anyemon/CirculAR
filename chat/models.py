from django.db import models
from Usuarios.models import CustomUser
from publicacion.models import Publicacion

# Create your models here.
class Meep(models.Model):
    user = models.ForeignKey(CustomUser, related_name="meeps", on_delete=models.DO_NOTHING)
    publicacion=models.IntegerField(null=False,blank=False)
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
        

    def __str__(self):
        return(
            f"{self.user}"
            f"({self.created_at:%Y-%m-%d %H:%M}):"
            f"{self.body}..."
        )