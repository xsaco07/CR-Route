"""cr_route URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inicio/', home, name='inicio'),
    path('rutas/', admin_rutas, name='rutas'),
    path('contacto/', admin_rutas, name='contacto'),
    path('acerca_de/', admin_rutas, name='acerca_de'),
    path('empresa/borrar/<int:id>/', borrar_empresa),
    path('empresa/insertar/', insertar_empresa),
    path('empresa/editar/<int:id>/', editar_empresa),
    path('empresa/listar/', listar_empresa, name='empresas'),
]
