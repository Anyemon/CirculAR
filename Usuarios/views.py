from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from .forms import *
from .models import CustomUser, Black_list
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from publicacion.models import Publicacion

# Create your views here.
def registrar(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method=='POST':
        form=RegistroForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                )
            login(request, user)
            messages.success(request,"Has ingresado correctamente..")
            return redirect('home')
    else:
        form=RegistroForm()
    context={
        'form':form
        }
    return render(request,'registro.html',context)

def ingresar(request):
    if request.method == 'POST':
        form = InicioSesionForm(request.POST)
        nameuser=request.POST['username']
        intentos=Black_list.objects.filter(login=nameuser, estado=0).count()
        if (intentos < 3):
                       
                       if form.is_valid():
                        
                        user = authenticate(
                            username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'],
                        )
                        if (user is None) or (user.estado == 'E'): 
                                                
                            print('Error con el usuario o la contraseña')
                            messages.error(request,'Error con el usuario o la contraseña')
                            Black_list.objects.create(login=nameuser)

                        else:
                            login(request, user)
                            messages.success(request,"Has ingresado correctamente..")
                            Black_list.objects.filter(login=nameuser).update(estado=1)
                            return redirect('home')
        else:
             messages.error(request,'su cuenta ha sido bloqueada, contactese con el administrador - Admin@CirculAR.com')



    else:
        form=InicioSesionForm()
    context={
            'form':form
            }
    return render(request, 'ingresar.html', context)

@login_required
def salir(request):
    logout(request)
    messages.success(request,"Has salido correctamente..")
    return render(request,'home.html',{})

@login_required
def modificar(request):
    usuario=request.user
    if request.method == 'POST':
        form = ModificarDatosForm(request.POST,request.FILES,instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('Usuarios:misDatos')
    elif request.method == 'GET':
        form=ModificarDatosForm(instance=usuario)
    context={
            'form':form
            }
    return render(request, 'modificar.html', context)

@login_required
def eliminar(request):
    if request.method == 'POST':
        form = EliminarForm(request.POST)
        Publicacion.objects.filter(usuario=request.user.id).update(vigencia=2)
        request.user.estado='E'
        request.user.save()
        logout(request)
        return redirect('home')
    else:
        form=EliminarForm()
    context={
            'form':form
            }
    return render(request, 'eliminar.html', context)

@login_required
def misDatos(request):
    if request.method == 'GET':
        usuario=request.user
    context={
            'usuario':usuario
            }
    return render(request, 'misDatos.html', context)
