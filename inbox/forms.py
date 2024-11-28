from django import forms
from .models import MensajeInbox

class NuevoMensajeInboxForm(forms.ModelForm):
    class Meta:
        model=MensajeInbox
        fields=[
            'cuerpo'
        ]
        labels={
            'cuerpo':'',
        }
        widgets={
            'cuerpo':forms.TextInput(attrs={'class':'form-control form-control-lg border border-primary','placeholder':'Nuevo mensaje...','size':'100'}),
        }
    
