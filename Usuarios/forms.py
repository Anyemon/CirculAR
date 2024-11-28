from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegistroForm(UserCreationForm):
    usable_password=None
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Nombre','class':'form-control'}), label='')
    last_name = forms.CharField(widget=forms.TimeInput(attrs={'placeholder':'Apellido','class':'form-control'}), label='')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Email','class':'form-control'}), label='', required=True)
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Nombre de Usuario','class':'form-control'}), label='')
    direccion = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Dirección','class':'form-control'}), label='')
    altura = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'Altura','class':'form-control'}), label='')
    fechaDeNacimiento = forms.DateField(widget=forms.DateTimeInput(attrs={'placeholder':'Fecha de Nacimiento','type':'date','class':'form-control'}), label='')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Contraseña','title':'''Ayuda: La contraseña es muy similar al nombre
            La contraseña es demasiado corta. Debe contener por lo menos 8 caracteres
            La contraseña tiene un valor demasiado común''','class':'form-control'}), label='', required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirmar contraseña','title':'Ayuda: La contraseñas deben coincidir','class':'form-control'}), label='', required=True)
    avatar=forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control'}),required=False,initial='images/sin_avatar.png')
    
    class Meta:
        model=CustomUser
        fields=['first_name','last_name','email','username','avatar','direccion','altura','fechaDeNacimiento','password1','password2']
    
    def save(self,commit=True):
        user=super(RegistroForm,self).save(commit=False)
        if commit:
            user.save()
        return user

class InicioSesionForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Nombre de Usuario','class':'form-control'}), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Contraseña','class':'form-control'}), label='', required=True)
    
    class Meta:
        fields=['username','password']

class ModificarDatosForm(ModelForm):
    class Meta:
        model=CustomUser
        fields=['first_name','last_name','avatar','fechaDeNacimiento','direccion','altura']
        labels={
            'first_name':'Nombre',
            'last_name':'Apellido',
            'avatar':'Avatar',
            'fechaDeNacimiento':'Fecha de nacimiento',
            'direccion':'Dirección',
            'altura':'Altura',
        }
        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'avatar':forms.FileInput(attrs={'class':'form-control'}),
            'fechaDeNacimiento':forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'direccion':forms.TextInput(attrs={'class':'form-control'}),
            'altura':forms.NumberInput(attrs={'class':'form-control'}),
        }

class EliminarForm(forms.Form):
    class Meta:
        model=CustomUser
