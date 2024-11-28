from django import forms
from .models import Rubro,Producto,Publicacion

class PublicacionForm(forms.ModelForm):
    class Meta:
        model=Publicacion
        fields=['nombre','descripcion','rubro','estado','valor','descuento']
        labels={
            'nombre':'',
            'descripcion':'',
            'rubro':'',
            'estado':'',
            'valor':'',
            'descuento':'',
        }        
        widgets = {
            'nombre':forms.TextInput(attrs={'placeholder':'Título','class':'form-control'}),
            'descripcion':forms.TextInput(attrs={'placeholder':'Descripción','class':'form-control'}),
            'rubro':forms.Select(attrs={'placeholder':'Rubro','class':'form-select'}),
            'estado':forms.Select(attrs={'placeholder':'Estado','class':'form-select'}),
            'valor':forms.NumberInput(attrs={'placeholder':'Precio','class':'form-control'}),
            'descuento':forms.NumberInput(attrs={'placeholder':'Descuento','class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rubro']=forms.ModelChoiceField(
            queryset=Rubro.objects.all(),empty_label='Rubro',
            widget=forms.Select(attrs={'class':'form-select'}),
            label=''
        )

class ProductoForm(forms.ModelForm):
    class Meta:
        model=Producto
        fields=['nombre','descripcion','imagen_1','imagen_2','imagen_3']
        labels = {
            'nombre':'',
            'descripcion':'',
            'imagen_1':'',
            'imagen_2':'',
            'imagen_3':'',
        }
        widgets = {
            'nombre':forms.TextInput(attrs={'placeholder':'Nombre del producto','class':'form-control'}),
            'descripcion':forms.TextInput(attrs={'placeholder':'Detalles técnicos del producto','class':'form-control'}),
            'imagen_1':forms.FileInput(attrs={'class':'form-control'}),
            'imagen_2':forms.FileInput(attrs={'class':'form-control'}), 
            'imagen_3':forms.FileInput(attrs={'class':'form-control'}),
        }

class ModificarProductoForm(forms.ModelForm):
    class Meta:
        model=Producto
        fields=['nombre','descripcion','imagen_1','imagen_2','imagen_3']
        labels = {
            'nombre':'Nombre del Producto',
            'descripcion':'Descripcion del Producto',
            'imagen_1':'Imagen 1',
            'imagen_2':'Imagen 2',
            'imagen_3':'Imagen 3',
        }
        widgets = {
            'nombre':forms.TextInput(attrs={'class':'form-control'}),
            'descripcion':forms.TextInput(attrs={'class':'form-control'}),
            'imagen_1':forms.FileInput(attrs={'class':'form-control'}),
            'imagen_2':forms.FileInput(attrs={'class':'form-control'}), 
            'imagen_3':forms.FileInput(attrs={'class':'form-control'}),
        }
        
class ModificarPublicacionForm(forms.ModelForm):
    class Meta:
        model=Publicacion
        fields=['nombre','descripcion','rubro','estado','valor','descuento']
        labels = {
            'nombre':'Nombre de la publicación',
            'descripcion':'Descripcion de la publicación',
            'rubro':'Rubro del producto',
            'estado':'Estado del producto',
            'valor':'Precio',
            'descuento':'Descuento',
        }
        widgets = {
            'nombre':forms.TextInput(attrs={'class':'form-control'}),
            'descripcion':forms.TextInput(attrs={'class':'form-control'}),
            'rubro':forms.Select(attrs={'class':'form-select'}),
            'estado':forms.Select(attrs={'class':'form-select'}),
            'valor':forms.NumberInput(attrs={'class':'form-control'}),
            'descuento':forms.NumberInput(attrs={'class':'form-control'}),         
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rubro']=forms.ModelChoiceField(
            queryset=Rubro.objects.all(),empty_label='Rubro',
            widget=forms.Select(attrs={'class':'form-select'})
        )

class EliminarPublicacionForm(forms.ModelForm):
    class Meta:
        model=Publicacion
        fields=['nombre','descripcion','rubro']
        labels = {
            'nombre':'Nombre de la publicación',
            'descripcion':'Descripcion de la publicación',
            'rubro':'Rubro del producto',
        }
        widgets = {
            'nombre':forms.TextInput(attrs={'class':'form-control'}),
            'descripcion':forms.TextInput(attrs={'class':'form-control'}),
            'rubro':forms.Select(attrs={'class':'form-select'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields:
            self.fields[campo].disabled=True
            