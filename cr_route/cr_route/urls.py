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
    path('empresa/listar/', listar_empresa, {"meta": False}, name='empresas'),
    path('empresa/listar/meta/', listar_empresa, {"meta": True}),
    path('ruta/listar/', listar_rutas, {"meta": False}, name='rutas'),
    path('ruta/listar/meta/', listar_rutas, {"meta": True}),
    path('ruta/editar/<int:id>/', editar_ruta, name='editar_ruta'),
    path('ruta/insertar/', insertar_ruta, name='insertar_ruta'),
    path('ruta/borrar/<int:id>/', borrar_ruta, name='borrar_ruta'),
    path('registro/', registrar_usuario),
    path('usuario/editar/<int:id>/', editar_usuario),
    path('usuario/borrar/<int:id>/', borrar_usuario),
    path('login/', iniciar_sesion),
    path('logout/', salir_sesion),
    path('contacto/', contacto),
    path('buscar_logs/', buscar_logs),
    path('', home),
    path('api/rutas_por_empresa/<int:id>/', api_rutas_por_empresa),
    path('api/ruta_por_id/<int:id_ruta>/', api_ruta_por_id),
    path('api/rutas_dentro/<str:lat1>,<str:lon1>/<str:lat2>,<str:lon2>/<str:criterio>/', api_rutas_dentro),
    path('buscar_rutas/', buscar_rutas),
    path('api/buscar_logs/<slug:fecha_inicio>/<slug:fecha_fin>/', api_buscar_logs),
    path('api/rutas_dentro/<str:lat1>,<str:lon1>/<str:lat2>,<str:lon2>/', api_rutas_dentro),
    path('api/rutas_por_tiempo/<int:minutos>/', api_rutas_por_tiempo),
    path('api/parada_mas_cercana/<str:usr_lat>,<str:usr_long>/<str:dest_lat>,<str:dest_long>/<int:rampa_required>', api_parada_mas_cercana),

]
