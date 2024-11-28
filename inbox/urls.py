from django.urls import path
from . import views

app_name='inbox'
urlpatterns = [
    path('inbox',views.inbox,name='inbox'),
    path('conversacion/<conversacion_id>',views.inbox,name='inbox'),
]