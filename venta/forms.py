from django import forms
from .models import Trueque

class RespuestaTruequeForm(forms.ModelForm):
    class Meta:
        model = Trueque
        fields = ['estado_trueque']
        widgets = {
            'estado_trueque': forms.Select(choices=[('aceptado', 'Aceptar'), ('rechazado', 'Rechazar')]),
        }
