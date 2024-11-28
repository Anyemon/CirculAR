from django.urls import path
from . import views


app_name = 'api'
urlpatterns = [
    path('procesar_pago/<int:publicacion_id>/', views.procesar_pago, name='procesar_pago'),
    path('pago_exitoso/', views.pago_exitoso, name='pago_exitoso'),
    path('pago_fallido/', views.pago_fallido, name='pago_fallido'),
    path('pago_pendiente/', views.pago_pendiente, name='pago_pendiente'),
]
