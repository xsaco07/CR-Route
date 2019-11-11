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
    path('empresa/borrar/<int:id>/', borrar_empresa, name='borrar_empresa'),
    path('empresa/insertar/', insertar_empresa, name='insertar_empresa'),
    path('empresa/editar/<int:id>/', editar_empresa, name='editar_empresa'),
    path('empresa/listar/', listar_empresa, {"meta":False}, name='empresas'),
    path('empresa/listar/meta/', listar_empresa, {"meta":True}),
    path('ruta/listar/', listar_rutas, name='rutas'),
    path('ruta/editar/<int:id>/', editar_ruta, name='editar_ruta'),
    path('ruta/insertar/', insertar_ruta, name='insertar_ruta'),
    path('ruta/borrar/<int:id>/', borrar_ruta, name='borrar_ruta'),
    path('registro/', registrar_usuario),
    path('usuario/editar/<int:id>/', editar_usuario),
    path('usuario/borrar/<int:id>/', borrar_usuario),
    path('login/', iniciar_sesion),
    path('logout/', salir_sesion),
    path('contacto/', contacto),
    path('', home),
    path('api/rutas_por_empresa/<int:id>/', api_rutas_por_empresa),
    path('api/ruta_por_numero/<int:num_ruta>/', api_puntos_por_num_ruta),
    path('api/rutas_dentro/<slug:lat1>,<slug:lon1>/<slug:lat2>,<slug:lon2>/', api_api_rutas_dentro),
]
