from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from app.models import *
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def home(request):
    return render(request, 'home.html')

def admin_rutas(request):
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
        context = empresa.__dict__
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

# Form vacío
def borrar_ruta(request, id):
    Ruta.objects.filter(id=id)[0].delete()
    return redirect('/inicio/')

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
        context = ruta.__dict__
        context["action"] = "/ruta/editar/"+str(id)+"/"
        return render(request, "form_ruta.html", context=context)


def listar_rutas(request):
    return render(request, 'admRutas.html')

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
        return render(request, "form_ruta.html", context=context)

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
        return redirect('/iniciar_sesion/')
    elif request.method == "GET":
        context = {"action": "/registro/"}
        return render(request, "registro.html", context=context)

@csrf_exempt
def iniciar_sesion(request):
    if request.method == "POST":
        data = request.POST
        nombre_usuario = data["nombre_usuario"]
        contrasena = data["contrasena"]
        try:
            usuario = Usuario.objects.filter(nombre_usuario=nombre_usuario)[0]
            if usuario.nombre_usuario == nombre_usuario and usuario.contrasena == contrasena:
                return redirect('/inicio/')
            messages.info(request, 'Nombre de usuario o contraseña incorrecta!')
            return render(request, "iniciar_sesion.html")
        except:
            messages.info(request, 'Nombre de usuario o contraseña incorrecta!')
            return render(request, "iniciar_sesion.html")

    elif request.method == "GET":
        return render(request, "iniciar_sesion.html")
