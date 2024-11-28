from django.shortcuts import get_object_or_404,render,redirect
from django.contrib.auth.decorators import login_required
from .forms import PublicacionForm,ProductoForm,ModificarProductoForm,ModificarPublicacionForm,EliminarPublicacionForm
from .models import Publicacion,Producto,CustomUser, Rubro
from django.forms.models import inlineformset_factory
from chat.models import Meep
from chat.forms import MeepForm
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from inbox.views import notificacion

# Create your views here.
@login_required
def nuevaPublicacion(request):

    lista_publicaciones = Publicacion.objects.all().order_by('-id').filter(usuario=request.user.id, vigencia=1)

    submitted = False

    # Definición del FormSet
    PublicacionFormSet = inlineformset_factory(
        Producto, 
        Publicacion, 
        form=PublicacionForm, 
        fields=['nombre', 'descripcion', 'rubro', 'estado', 'valor', 'descuento'],
        can_delete=False, 
        extra=1
    )

    # Inicializa el formulario y el FormSet
    form = ProductoForm()
    publicacionFormSet = PublicacionFormSet()

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save()
            publicacionFormSet = PublicacionFormSet(request.POST, instance=producto)
            if publicacionFormSet.is_valid():
                publicaciones = publicacionFormSet.save(commit=False)
                for publicacion in publicaciones:
                    publicacion.usuario = request.user
                    publicacion.save()
                submitted = True
            else:
                # Eliminar el producto si hubo un error con el FormSet
                producto.delete()
                messages.error(request, "Ha ocurrido un error al cargar la publicación...")
        else:
            # Inicializar FormSet vacío en caso de que el formulario `ProductoForm` no sea válido
            publicacionFormSet = PublicacionFormSet()

    context = {
        'form': form,
        'publicacionFormSet': publicacionFormSet,
        'submitted': submitted,
        'lista_publicaciones': lista_publicaciones
    }

    return render(request, 'nueva_publicacion.html', context)

#@login_required
#def lista_publicaciones(request):
 #   lista_publicaciones = Publicacion.objects.all().order_by('-id').filter(usuario=request.user.id).exclude(vigencia=2)
  #  context={
   #     'lista_publicaciones': lista_publicaciones
    #}
    #return render(request,'lista_publicaciones.html',context)

@login_required
def lista_publicaciones(request):

    lista_publicaciones = Publicacion.objects.all().order_by('-id').filter(usuario=request.user.id, vigencia=1).exclude(vigencia=2)
    context={
    # Filtrar publicaciones del usuario actual que estén en estado "VIGENTE" (excluir ELIMINADO y SUSPENDIDO)
        'lista_publicaciones': lista_publicaciones
    }
    return render(request, 'lista_publicaciones.html', context)

   
def publicaciones(request):
    rubros=Rubro.objects.all()
    publicacion = Publicacion.objects.all().filter(vigencia=1).order_by('-id')
    p = Paginator(Publicacion.objects.all().filter(vigencia=1).order_by('-id'), 6)
    page= request.GET.get('page' )
    pub=p.get_page(page)
    nums = "a" * pub.paginator.num_pages

    context={
        'rubros': rubros,
        'publicacion': publicacion,
        'pub': pub,
        'nums': nums
    }
    return render(request,'publicaciones.html',context)

    
def publicaciones_filtradas(request, id):
    rubros=Rubro.objects.all()
    if id < 5:
       publicacion = Publicacion.objects.all().filter(rubro=id, vigencia=1).order_by('-id')
       p = Paginator(Publicacion.objects.all().filter(rubro=id, vigencia=1).order_by('-id'),6)
       page= request.GET.get('page' )
       pub=p.get_page(page)
       nums = "a" * pub.paginator.num_pages

    elif id == 5:
        publicacion = Publicacion.objects.all().filter(vigencia=1).order_by('id')
        p = Paginator(Publicacion.objects.all().filter(vigencia=1).order_by('id'),6)
        page= request.GET.get('page' )
        pub=p.get_page(page)
        nums = "a" * pub.paginator.num_pages

    elif id == 6:
        publicacion = Publicacion.objects.all().filter(vigencia=1).order_by('-id')
        p = Paginator(Publicacion.objects.all().filter(vigencia=1).order_by('-id'),6)
        page= request.GET.get('page' )
        pub=p.get_page(page)
        nums = "a" * pub.paginator.num_pages

    elif id == 7:
        publicacion = Publicacion.objects.all().filter(vigencia=1).order_by('-valor')
        p = Paginator(Publicacion.objects.all().filter(vigencia=1).order_by('-valor'),6)
        page= request.GET.get('page' )
        pub=p.get_page(page)
        nums = "a" * pub.paginator.num_pages

    elif id == 8:
        publicacion = Publicacion.objects.all().filter(vigencia=1).order_by('valor')
        p = Paginator(Publicacion.objects.all().filter(vigencia=1).order_by('valor'),6)
        page= request.GET.get('page' )
        pub=p.get_page(page)
        nums = "a" * pub.paginator.num_pages      

    context={
        'publicacion': publicacion,
        'id': id,
        'pub': pub,
        'nums': nums,
        'rubros': rubros
    }
    return render(request,'publicaciones_filtradas.html',context)


@login_required
def mostrar_publicacion(request, id):
    publicacion = get_object_or_404(Publicacion, pk=id)
    
    # Obtener el nombre del estado
    estado_nombre = publicacion.get_estado_display()

    if request.method == "POST":
        form = MeepForm(request.POST or None)

        publica=get_object_or_404(Publicacion,pk=id)
        if request.method == "POST":
            if form.is_valid():
                meep = form.save(commit=False)
                meep.user = request.user
                meep.publicacion=publica.id
                meep.save()
                notificacion(request,publica,1)
                messages.success(request, ('Tu consulta ha sido publicada'))
                return redirect('publicacion:mostrar_publicacion', publica.id)
        publicacion=get_object_or_404(Publicacion,pk=id)
        publicados=Publicacion.objects.all().filter(usuario=publicacion.usuario,vigencia=1).exclude(pk=id)[:4]
        vendedor=CustomUser.objects.all().filter(username=publicacion.usuario)
        meeps=Meep.objects.all().filter(publicacion=id).order_by("-created_at")
        meeps_cantidad=Meep.objects.filter(publicacion=id).count()
        Publicacion.objects.filter(pk=id).update(comentarios=meeps_cantidad)
        context={
            'publicacion':publicacion,
            'publicados':publicados,
            'vendedor' :vendedor,
            'meeps':meeps,
            'meeps_cantidad': meeps_cantidad, 
            'form':form
        }
        return render(request,'mostrar_publicacion.html',context)
    
    else:
        publicacion=get_object_or_404(Publicacion,pk=id)
        publicados=Publicacion.objects.all().filter(usuario=publicacion.usuario,vigencia=1).exclude(pk=id)[:4]
        vendedor=CustomUser.objects.all().filter(username=publicacion.usuario)
        meeps=Meep.objects.all().filter(publicacion=id).order_by("-created_at")
        form = MeepForm(request.POST or None) if request.user.is_authenticated else None
        context={
            'publicacion':publicacion,
            'publicados':publicados,
            'vendedor' :vendedor,
            'form': form,
            'meeps':meeps
        }
        return render(request,'mostrar_publicacion.html',context)
    
   
@login_required
def modificar_publicacion(request,id):
    publicacion=get_object_or_404(Publicacion,pk=id)
    producto=get_object_or_404(Producto,pk=publicacion.producto.pk)
    PublicacionFormSet = inlineformset_factory(Producto,Publicacion,form=ModificarPublicacionForm,fields=['nombre','descripcion','rubro','estado','valor','descuento'],can_delete=False,max_num=1)
    if request.method == 'POST':
        form=ModificarProductoForm(request.POST, request.FILES, instance=producto)
        publicacionFormSet = PublicacionFormSet(request.POST,instance=producto)
        if form.is_valid() and publicacionFormSet.is_valid():
            form.save()
            publicacionFormSet.save()
            context={
                'publicacion':get_object_or_404(Publicacion,pk=id)
            }
            messages.success(request,"La publicación ha sido actualizada")
            return render(request,'mostrar_publicacion.html',context)
    else:
        form = ModificarProductoForm(instance=producto)
        publicacionFormSet=PublicacionFormSet(instance=producto)
    context={
        'form':form,
        'publicacionFormSet':publicacionFormSet,
        'publicacion':publicacion
    }
    return render(request,'modificar_publicacion.html',context)

@login_required
def eliminar_publicacion(request,id):
    publicacion=get_object_or_404(Publicacion,pk=id)
    if request.method == 'POST':
        publicacion.vigencia=2
        publicacion.save()
        messages.success(request,"La publicación se ha eliminado")
        return redirect('publicacion:lista_publicaciones')
    else:
        form=EliminarPublicacionForm(instance=publicacion)
    context={
            'form':form
            }
    return render(request, 'eliminar_publicacion.html', context)

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        if searched != '':
            #busco los productos
            searched = Publicacion.objects.filter(Q(nombre__icontains=searched) | Q(descripcion__icontains=searched)).filter(vigencia=1)
            total_search = searched.count()
            rubros=Rubro.objects.all()

            searched_1 = searched.filter(rubro=1)
            total_search_1 = searched_1.count()
            rubros_1 = rubros.filter(id=1)

            searched_2 = searched.filter(rubro=2)
            total_search_2 = searched_2.count()
            rubros_2 = rubros.filter(id=2)

            searched_3 = searched.filter(rubro=3)
            total_search_3 = searched_3.count()
            rubros_3 = rubros.filter(id=3)

            searched_4 = searched.filter(rubro=4)
            total_search_4 = searched_4.count()
            rubros_4 = rubros.filter(id=4)
        else:
            messages.warning(request,"Tienes que poner algo en la busqueda...intentalo de nuevo! ")
            return render(request, "buscar_publicacion.html", {})

        
        #sino encuentro nada
        if not searched:
            messages.warning(request,"No encontramos lo que buscabas...intentalo de nuevo! ")
            return render(request, "buscar_publicacion.html", {})
        else:
           return render(request, "buscar_publicacion.html", {'searched':searched, 'total_search': total_search, 
                                                              'searched_1':searched_1, 'searched_2':searched_2,
                                                              'searched_3': searched_3, 'searched_4': searched_4,
                                                              'total_search_1': total_search_1,'total_search_2': total_search_2,
                                                              'total_search_3':total_search_3, 'total_search_4': total_search_4,
                                                              'rubros_1':rubros_1, 'rubros_2': rubros_2, 
                                                              'rubros_3': rubros_3, 'rubros_4':rubros_4})
    else:
     return render(request, 'buscar_publicacion.html', {})

@login_required
def confirmar_pago(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)

    if request.method == 'POST':
        # Cambiar el estado de la publicación a "SUSPENDIDO"
        publicacion.estado = 3  # SUSPENDIDO (de acuerdo con ELECCION_VIGENCIA)
        publicacion.save()

        # Mensaje de éxito
        messages.success(request, "El pago ha sido confirmado y la publicación se ha suspendido correctamente.")

        # Redirigir a la página de compras realizadas o donde prefieras
        return redirect('compra:compras_realizadas')

    return render(request, 'confirmar_pago.html', {'publicacion': publicacion})