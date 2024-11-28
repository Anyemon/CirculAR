from django.urls import path
from . import views

app_name = 'publicacion'
urlpatterns = [
    path('publicaciones',views.publicaciones,name='publicaciones'),
    path('publicaciones_filtradas/<int:id>',views.publicaciones_filtradas,name='publicaciones_filtradas'),
    path('nueva_publicacion',views.nuevaPublicacion,name='nuevaPublicacion'),
    path('lista_publicaciones',views.lista_publicaciones,name='lista_publicaciones'),
    path('mostrar_publicacion/<int:id>',views.mostrar_publicacion,name='mostrar_publicacion'),
    path('modificar_publicacion/<int:id>',views.modificar_publicacion,name='modificar_publicacion'),
    path('eliminar_publicacion/<int:id>',views.eliminar_publicacion,name='eliminar_publicacion'),
    path ('buscar_publicacion', views.search, name='buscar_publicacion'),
]