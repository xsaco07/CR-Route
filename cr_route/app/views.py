from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from app.models import *
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def home(request):
    return render(request, 'home.html')


# Form vacío
def borrar_empresa(request, id):
    Empresa.objects.filter(id=id)[0].delete()
    return HttpResponse("OK")



@csrf_exempt 
def editar_empresa(request, id):
    empresa = Empresa.objects.filter(id=id)[0]
    if request.method == "POST":
        data = request.POST
        empresa.nombre = data["nombre"]
        empresa.zona = data["zona"]
        empresa.telefono = data["telefono"]
        empresa.correo = data["correo"]
        empresa.direccion = data["direccion"]
        empresa.latitud = data["latitud"]
        empresa.longitud = data["longitud"]
        empresa.horario = data["horario"]
        empresa.save()
        return HttpResponse("OK")
    elif request.method == "GET":
        context = empresa.__dict__
        context["action"] = "/empresa/editar/"+str(id)+"/"
        return render(request, "form_empresa.html", context=context)


def listar_empresa(request):
    pass

@csrf_exempt 
def insertar_empresa(request):
    if request.method == "POST":
        data = request.POST
        empresa = Empresa()
        empresa.nombre = data["nombre"]
        empresa.zona = data["zona"]
        empresa.telefono = data["telefono"]
        empresa.correo = data["correo"]
        empresa.direccion = data["direccion"]
        empresa.latitud = data["latitud"]
        empresa.longitud = data["longitud"]
        empresa.horario = data["horario"]
        empresa.save()
        return HttpResponse("OK")
    elif request.method == "GET":
        context = {"action":"/empresa/insertar/"}
        return render(request, "form_empresa.html", context=context)

@csrf_exempt
def registro(request):
    if request.method == "POST":
        data = request.POST
        usuario = Usuario()
        usuario.nombre_usuario = data["nombre_usuario"]
        usuario.nombre = data["nombre"]
        usuario.apellido1 = data["apellido1"]
        usuario.apellido2 = data["apellido2"]
        usuario.contrasena = data["contrasena"]
        usuario.save()
        return redirect('/login/')
    elif request.method == "GET":
        context = {"action": "/registro/"}
        return render(request, "registro.html", context=context)

@csrf_exempt
def login(request):
    if request.method == "POST":
        data = request.POST
        nombre_usuario = data["nombre_usuario"]
        contrasena = data["contrasena"]
        try:
            usuario = Usuario.objects.filter(nombre_usuario=nombre_usuario)[0]
            if usuario.nombre_usuario == nombre_usuario and usuario.contrasena == contrasena:
                return redirect('/home/')
            messages.info(request, 'Nombre de usuario o contraseña incorrecta!')
            return render(request, "login.html")
        except:
            messages.info(request, 'Nombre de usuario o contraseña incorrecta!')
            return render(request, "login.html")

    elif request.method == "GET":
        return render(request, "login.html")
