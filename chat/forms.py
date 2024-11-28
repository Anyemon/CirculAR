from django import forms
from .models import Meep

class MeepForm(forms.ModelForm):
    body = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={
            "placeholder":"Ingrese su pregunta",
            "class":"form-control",
        }

    ), label="" )

    class Meta:
        model = Meep
        exclude = ("user","publicacion")