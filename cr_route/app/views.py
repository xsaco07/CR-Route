from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from app.models import *
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

# Create your views here.

def home(request):
    context = {"usuario" : "Sin usuario"}
    return render(request, 'home.html', context=context)

def listar_rutas(request):
    rutas = Ruta.objects.all()
    return render(request, 'admRutas.html', {'rutas':rutas})

def borrar_ruta(request, id):
    Ruta.objects.filter(id=id)[0].delete()
    return redirect('/ruta/listar')

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

        crear_paradas(data, ruta)

        return redirect('/ruta/listar')

    elif request.method == "GET":

        paradas = Parada.objects.filter(ruta=ruta).order_by('serial')
        paradas_coords = []

        for parada in paradas:
            print(parada.longitud)
            paradas_coords += [[parada.latitud, parada.longitud]]

        context = model_to_dict(ruta)
        context["action"] = "/ruta/editar/"+str(id)+"/"
        context['paradas'] = paradas_coords
        return render(request, "editar_crear_rutas.html", context=context)

@csrf_exempt
def insertar_ruta(request):

    if request.method == "POST":
        # Crear nueva Ruta
        data = request.POST
        ruta = Ruta()
        ruta.empresa = Empresa.objects.last()
        ruta.numero_ruta = data["numero_ruta"]
        ruta.descripcion = data["descripcion"]
        ruta.precio = data["precio"]
        ruta.horario = data["horario"]
        ruta.duracion = data["duracion"]
        ruta.rampa = data["rampa"]
        ruta.save()

        crear_paradas(data, ruta)

        messages.info(request, 'Ruta creada exitosamente.')
        return listar_rutas(request)

    elif request.method == "GET":
        context = {"action":"/ruta/insertar/"}
        return render(request, "editar_crear_rutas.html", context=context)

def crear_paradas(data, ruta):
    # Convert string to list of floats
    coordenates = data['puntos'].split(',')
    coordenates = list(map(float, coordenates))

    # Create matrix of points
    final_coordenates = list(divide_chunks(coordenates, 2))

    # Borrar paradas previamente asociadas
    Parada.objects.filter(ruta=ruta).delete()

    # Crear nuevas Paradas
    serial = 1;
    for par in final_coordenates:
        parada = Parada()
        parada.ruta = ruta
        parada.serial = serial
        parada.latitud = par[0]
        parada.longitud = par[1]
        parada.save()
        serial += 1

# Divide list in chunks
def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

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

def listar_empresa(request, meta):
    empresas = Empresa.objects.all()
    if(meta):
        # only return metadata id and name
        return render(request,"combo_options.html",{"empresas":empresas})
    else:
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

@csrf_exempt
def registrar_usuario(request):
    if request.method == "POST":
        data = request.POST
        usuario = Usuario()
        usuario.nombre_usuario = data["nombre_usuario"]
        usuario.nombre = data["nombre"]
        usuario.apellido1 = data["apellido1"]
        usuario.apellido2 = data["apellido2"]
        usuario.contrasena = data["contrasena"]
        try:
            usuario = Usuario.objects.filter(nombre_usuario=usuario.nombre_usuario)[0]
            if usuario.nombre_usuario == data["nombre_usuario"]:
                context = {"mensaje": "Nombre de usuario ya existente, intente con otro diferente."}
                context["titulo"] = "Nombre usuario"
                return render(request, "registrar_usuario.html", context=context)
        except:
            usuario.save()
            context = {"mensaje": 'Usuario creado exitosamente.'}
            return render(request, "iniciar_sesion.html", context=context)
    elif request.method == "GET":
        context = {"action": "/registro/"}
        context["titulo"] = "Nombre usuario"
        return render(request, "registrar_usuario.html", context=context)

@csrf_exempt
def iniciar_sesion(request):
    if request.method == "POST":
        data = request.POST
        nombre_usuario = data["nombre_usuario"]
        contrasena = data["contrasena"]
        try:
            usuario = Usuario.objects.filter(nombre_usuario=nombre_usuario)[0]
            if usuario.nombre_usuario == nombre_usuario and usuario.contrasena == contrasena:
                context = {"usuario": "Con usuario"}
                context["id"] = usuario.id
                return render(request, "home.html", context=context)
            context = {"mensaje": 'El nombre de usuario o contraseña que has introducido es incorrecta'}
            return render(request, "iniciar_sesion.html", context=context)
        except:
            context = {"mensaje": 'El nombre de usuario o contraseña que has introducido es incorrecta'}
            return render(request, "iniciar_sesion.html", context=context)

    elif request.method == "GET":
        return render(request, "iniciar_sesion.html")

@csrf_exempt
def editar_usuario(request, id):
    usuario = Usuario.objects.filter(id=id)[0]
    if request.method == "POST":
        data = request.POST
        usuario.nombre = data["nombre"]
        usuario.apellido1 = data["apellido1"]
        usuario.apellido2 = data["apellido2"]
        usuario.contrasena = data["contrasena"]
        usuario.save()
        context = {"mensaje": 'Usuario editado exitosamente'}
        return render(request,"iniciar_sesion.html", context=context)
    elif request.method == "GET":
        context = model_to_dict(usuario)
        context["action"] = "/usuario/editar/"+str(id)+"/"
        context["titulo"] = "Editar usuario"
        return render(request, "registrar_usuario.html", context=context)

@csrf_exempt
def borrar_usuario(request, id):
    Usuario.objects.filter(id=id)[0].delete()
    context = {"mensaje": 'Usuario borrado correctamente.'}
    return render(request,"iniciar_sesion.html", context=context)
