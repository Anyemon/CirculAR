from django.urls import path
from . import views

app_name='Usuarios'
urlpatterns = [
    path('registrar',views.registrar,name='registrar'),
    path('salir',views.salir,name='salir'),
    path('ingresar',views.ingresar,name='ingresar'),
    path('modificar',views.modificar,name='modificar'),
    path('eliminar',views.eliminar,name='eliminar'),
    path('misDatos',views.misDatos,name='misDatos'),
]