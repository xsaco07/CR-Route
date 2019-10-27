from django.shortcuts import render
from django.http import HttpResponse
from app.models import *
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def home(request):
    return render(request, 'home.html')

def listar_rutas(request):
    # Esta parte es de prueba
    # Creo una ruta y la paso por el context cada vez que se solicita la página
    # TODO: implementar el formulario de crear rutas para quitar esto
    empresas = Empresa.objects.all()
    empresa_id = empresas[0].id
    new_route = Ruta(empresa=empresas[0], descripcion="descripcion", precio=50, horario="lunes a viernes", duracion=30, rampa=False)
    new_route.save()
    rutas = Ruta.objects.all()
    print(rutas)
    return render(request, 'admRutas.html', {'rutas':rutas})

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
    return render(request, 'admEmpresas.html')

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
