"""
URL configuration for PruebaCirculAR project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('', include('Usuarios.urls',namespace='Usuarios')),
    path('', include('publicacion.urls',namespace='publicacion')),
    path('', include('compra.urls', namespace='compra')),
    path('',include('api.urls', namespace='api')),
    path('', include('inbox.urls',namespace='inbox')),
    path('', include('venta.urls',namespace='venta')),
    path('acerca/', views.acerca, name='acerca'),
    path('faq/', views.faq, name='faq'),
    path('terminos/', views.terminos, name='terminos'),
    path('privacidad/', views.privacidad, name='privacidad'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
