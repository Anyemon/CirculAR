from django.urls import path
from . import views

app_name = 'venta'
urlpatterns = [
    #path('venta/ventas_realizadas/', views.ventas_realizadas, name='ventas_realizadas'),
    path('ventas_realizadas/', views.ventas_realizadas, name='ventas_realizadas'),
    path('trueque/<int:trueque_id>/responder/<str:accion>/', views.responder_trueque, name='responder_trueque'),
    ]
