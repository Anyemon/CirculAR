from django import forms
from .models import Compra, Trueque

 

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['numeroComprobante', 'imagen', 'fechaDeTransferencia']

        labels = {
            'numeroComprobante':'comprobante',
            'imagen':'adjuntar archivo',
            'fechaDeTransferencia':'fecha Transferencia ',
            
            
                 }
        
        widgets = {
            'numeroComprobante':forms.TextInput(attrs={'class':'form-control ms-4', 'style':'width: 103%'}),
            'fechaDeTransferencia':forms.DateInput(attrs={'type':'date','class':'form-control ms-4', 'style':'width: 103%'}),
            'imagen':forms.FileInput(attrs={'class':'form-control ms-4', 'style':'width: 103%'}),
            
        }
       
            
class TruequeForm(forms.ModelForm):
    class Meta:
        model = Trueque
        fields = ['producto_ofrecido', 'imagen1', 'imagen2']
        labels = {
            'producto_ofrecido':'',
            'imagen1':'',
            'imagen2':'',
             }
        widgets = {
            'producto_ofrecido': forms.Textarea(attrs={'placeholder': 'Describe el producto que ofreces para el trueque','class':'form-control mt-2', 'style':'width: 108%;'}),
            'imagen1':forms.FileInput(attrs={'class':'form-control', 'style':'width: 108%;'}),
            'imagen2':forms.FileInput(attrs={'class':'form-control', 'style':'width: 108%;'}),
        }