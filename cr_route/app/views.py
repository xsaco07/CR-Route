from django.shortcuts import render, redirect
from django.http import HttpResponse
from app.models import *
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

# Create your views here.

def home(request):
    return render(request, 'home.html')

def listar_rutas(request):
    rutas = Ruta.objects.all()
    return render(request, 'admRutas.html', {'rutas':rutas})

def borrar_ruta(request, id):
    Ruta.objects.filter(id=id)[0].delete()
    return listar_rutas(request)

@csrf_exempt
def editar_ruta(request, id):
    ruta = Ruta.objects.filter(id=id)[0]
    if request.method == "POST":
        data = request.POST
        ruta.empresa = Empresa.objects.last()
        ruta.descripcion = data["descripcion"]
        ruta.precio = data["precio"]
        ruta.horario = data["horario"]
        ruta.duracion = data["duracion"]
        ruta.rampa = data["rampa"]
        ruta.save()
        return redirect('/inicio/')
    elif request.method == "GET":
        context = model_to_dict(ruta)
        context["action"] = "/ruta/editar/"+str(id)+"/"
        return render(request, "editar_crear_rutas.html", context=context)

@csrf_exempt
def insertar_ruta(request):
    if request.method == "POST":
        data = request.POST
        ruta = Ruta()
        ruta.empresa = Empresa.objects.last()
        ruta.descripcion = data["descripcion"]
        ruta.precio = data["precio"]
        ruta.horario = data["horario"]
        ruta.duracion = data["duracion"]
        ruta.rampa = data["rampa"]
        ruta.save()
        return redirect('/inicio/')
    elif request.method == "GET":
        context = {"action":"/ruta/insertar/"}
        return render(request, "editar_crear_rutas.html", context=context)

def borrar_empresa(request, id):
    Empresa.objects.filter(id=id)[0].delete()
    return render(request,"form_empresa.html",{
        "info_message":"Empresa borrada correctamente. ¿Te gustaría agregar una nueva?",
        "action":"/empresa/insertar/"})

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
        return render(request,"form_empresa.html",{
            "action":"empresa/insertar/",
            "info_message":"¡Datos actualizados correctamente!"
        })
    elif request.method == "GET":
        context = model_to_dict(empresa)
        context["action"] = "/empresa/editar/"+str(id)+"/"
        return render(request, "form_empresa.html", context=context)

def listar_empresa(request):
    empresas = Empresa.objects.all()
    context = {"empresas":empresas}
    return render(request, 'admEmpresas.html', context=context)

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
        return render(request, "form_empresa.html",{"info_message":"Empresa registrada exitosamente!"})
    elif request.method == "GET":
        context = {"action":"/empresa/insertar/"}
        return render(request, "form_empresa.html", context=context)
