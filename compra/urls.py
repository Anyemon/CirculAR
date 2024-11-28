from django.urls import path
from . import views
from .views import trueque_realizado

app_name = 'compra'
urlpatterns = [
path('realizar_compra/<int:id>/', views.realizar_compra, name='realizar_compra'),
path('compra/compras_realizadas/', views.compras_realizadas, name='compras_realizadas'),
path('pago_efectivo/<int:publicacion_id>/', views.pago_efectivo, name='pago_efectivo'),
path('pago_transferencia/<int:publicacion_id>/', views.pago_transferencia, name='pago_transferencia'),
path('trueque/<int:publicacion_id>/', views.trueque_view, name='trueque'),
path('compra/trueque_realizado/', trueque_realizado, name='trueque_realizado'),
path('compra/publicado/<int:publicacion_id>/', views.publicado, name='publicado'),
path('compra/nuevoproducto/<int:publicacion_id>/', views.nuevo_producto, name='nuevo_producto'),
]