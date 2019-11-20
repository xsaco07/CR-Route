from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from app.models import *
import json 
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

# Create your views here.

def home(request):
    try:
        context = {"id": request.session['id'], "session_key": request.session.session_key}
        return render(request, 'home.html', context=context)
    except:
        return render(request, 'home.html')

def listar_rutas(request, meta):
    rutas = Ruta.objects.all()
    try:
        if(meta):
            result = []
            for ruta in rutas:
                result.append({
                    "descripcion":ruta.descripcion,
                    "empresa":ruta.empresa.nombre,
                    "id":ruta.id
                    })
            return HttpResponse(json.dumps(result))
        context = {'rutas':rutas, "id": request.session['id'], "session_key": request.session.session_key}
        return render(request, 'admRutas.html', context=context)
    except:
        context = {'rutas':rutas}
        return render(request, 'admRutas.html', context=context)

def borrar_ruta(request, id):
    if request.session.session_key:
        Ruta.objects.filter(id=id)[0].delete()
        try:
            context = {"id": request.session['id'], "session_key": request.session.session_key}
            registrar_log(request.session['usuario_obj'], "Eliminó una ruta", "Ruta")
            return redirect('/ruta/listar', context=context)
        except:
            return redirect('/ruta/listar')
    else:
        return render(request, "home.html")

@csrf_exempt
def editar_ruta(request, id):
    if request.session.session_key:
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
            context = {"id": request.session['id'], "session_key": request.session.session_key}
            registrar_log(request.session['usuario_obj'], "Editó una ruta", "Ruta")
            return redirect('/ruta/listar', context=context)

        elif request.method == "GET":

            paradas = Punto.objects.filter(ruta=ruta).order_by('serial')
            paradas_coords = []

            for parada in paradas:
                print(parada.longitud)
                paradas_coords += [[parada.latitud, parada.longitud]]

            context = model_to_dict(ruta)
            context["action"] = "/ruta/editar/"+str(id)+"/"
            context['paradas'] = paradas_coords
            context["id"] = request.session['id']
            context["session_key"] = request.session.session_key
            return render(request, "editar_crear_rutas.html", context=context)
    else:
        return render(request, "home.html")

@csrf_exempt
def insertar_ruta(request):
    if request.session.session_key:
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
            registrar_log(request.session['usuario_obj'], "Registró una nueva ruta", "Ruta")
            return listar_rutas(request)

        elif request.method == "GET":
            context = {"action":"/ruta/insertar/", "id": request.session['id'], "session_key": request.session.session_key}
            return render(request, "editar_crear_rutas.html", context=context)
    else:
        return render(request, "home.html")

def crear_paradas(data, ruta):
    # Convert string to list of floats
    coordenates = data['puntos'].split(',')
    coordenates = list(map(float, coordenates))

    # Create matrix of points
    final_coordenates = list(divide_chunks(coordenates, 2))

    # Borrar paradas previamente asociadas
    Punto.objects.filter(ruta=ruta).delete()

    # Crear nuevas Paradas
    serial = 1;
    for par in final_coordenates:
        parada = Punto()
        parada.ruta = ruta
        parada.serial = serial
        parada.latitud = par[0]
        parada.longitud = par[1]
        parada.esParada = False #TODO quitar este valor quemado 
        parada.save()
        serial += 1

# Divide list in chunks
def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def borrar_empresa(request, id):
    if request.session.session_key:
        registrar_log(request.session['usuario_obj'], "Borró una empresa", "Empresa")
        Empresa.objects.filter(id=id)[0].delete()
        return render(request,"form_empresa.html",{
            "info_message":"Empresa borrada correctamente. ¿Te gustaría agregar una nueva?",
            "action":"/empresa/insertar/", "id": request.session['id'], "session_key": request.session.session_key})
    else:
        return render(request, "home.html")

@csrf_exempt
def editar_empresa(request, id):
    if request.session.session_key:
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
            registrar_log(request.session['usuario_obj'], "Editó una empresa", "Empresa")
            return render(request,"form_empresa.html",{
                "action":"empresa/insertar/",
                "info_message":"¡Datos actualizados correctamente!",
                "id": request.session['id'],
                "session_key": request.session.session_key
            })
        elif request.method == "GET":
            context = model_to_dict(empresa)
            context["action"] = "/empresa/editar/"+str(id)+"/"
            context["id"] = request.session['id']
            context["session_key"] = request.session.session_key
            return render(request, "form_empresa.html", context=context)
    else:
        return render(request, "home.html")

def listar_empresa(request, meta):
    empresas = Empresa.objects.all()
    if(meta):
        # only return metadata id and name
        return render(request,"combo_options.html",{"empresas":empresas, "id": request.session['id'], "session_key": request.session.session_key})
    else:
        try:
            context = {"empresas":empresas, "id": request.session['id'], "session_key": request.session.session_key}
            return render(request, 'admEmpresas.html', context=context)
        except:
            context = {"empresas":empresas}
            return render(request, 'admEmpresas.html', context=context)

@csrf_exempt
def insertar_empresa(request):
    if request.session.session_key:
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
            registrar_log(request.session['usuario_obj'], "Registró una nueva empresa", "Empresa")
            return render(request, "form_empresa.html",{"info_message":"Empresa registrada exitosamente!", "id": request.session['id'], "session_key": request.session.session_key})
        elif request.method == "GET":
            context = {"action":"/empresa/insertar/", "id": request.session['id'], "session_key": request.session.session_key}
            return render(request, "form_empresa.html", context=context)
    else:
        return render(request, "home.html")

@csrf_exempt
def registrar_usuario(request):
    if not request.session.session_key:
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
                context["action"] = "/login/"
                return render(request, "iniciar_sesion.html", context=context)
        elif request.method == "GET":
            context = {"action": "/registro/"}
            context["titulo"] = "Nombre usuario"
            return render(request, "registrar_usuario.html", context=context)
    else:
        return render(request, "home.html")

@csrf_exempt
def iniciar_sesion(request):
    if not request.session.session_key:
        if request.method == "POST":
            data = request.POST
            nombre_usuario = data["nombre_usuario"]
            contrasena = data["contrasena"]
            try:
                usuario = Usuario.objects.filter(nombre_usuario=nombre_usuario)[0]
                if usuario.nombre_usuario == nombre_usuario and usuario.contrasena == contrasena:
                    request.session.create()
                    request.session['id'] = usuario.id
                    request.session['usuario_obj'] = usuario
                    context = {"id": usuario.id, "session_key": request.session.session_key}
                    request.session.set_expiry(600)
                    registrar_log(request.session['usuario_obj'], "Inició sesión", "Usuario")
                    return render(request, "home.html", context=context)
                context = {"mensaje": 'La contraseña que has introducido es incorrecta'}
                return render(request, "iniciar_sesion.html", context=context)
            except:
                context = {"mensaje": 'El nombre de usuario que has introducido no existe'}
                return render(request, "iniciar_sesion.html", context=context)

        elif request.method == "GET":
            return render(request, "iniciar_sesion.html")
    else:
        context = {"session_key": request.session.session_key}
        return render(request, "home.html", context=context)

@csrf_exempt
def editar_usuario(request, id):
    if request.session.session_key:
        usuario = Usuario.objects.filter(id=id)[0]
        if request.method == "POST":
            data = request.POST
            usuario.nombre = data["nombre"]
            usuario.apellido1 = data["apellido1"]
            usuario.apellido2 = data["apellido2"]
            usuario.contrasena = data["contrasena"]
            usuario.save()
            context = {"mensaje": 'Usuario editado exitosamente', "action":"/login/"}
            registrar_log(request.session['usuario_obj'], "Editó su usuario", "Usuario")
            request.session.flush()
            return render(request,"iniciar_sesion.html", context=context)
        elif request.method == "GET":
            context = model_to_dict(usuario)
            context["action"] = "/usuario/editar/"+str(id)+"/"
            context["titulo"] = "Editar usuario"
            context["session_key"] = request.session.session_key
            context["id"] = request.session['id']
            return render(request, "registrar_usuario.html", context=context)
    else:
        return render(request, "home.html")

@csrf_exempt
def borrar_usuario(request, id):
    if request.session.session_key:
        Usuario.objects.filter(id=id)[0].delete()
        context = {"mensaje": 'Usuario borrado correctamente.', "action":"/login/"}
        registrar_log(request.session['usuario_obj'], "Eliminó su usuario", "Usuario")
        request.session.flush()
        return render(request,"iniciar_sesion.html", context=context)
    else:
        return render(request, "home.html")

@csrf_exempt
def salir_sesion(request):
    if request.session.session_key:
        registrar_log(request.session['usuario_obj'], "Cerró su sesion", "Usuario")
        request.session.flush()
        return redirect("/login/")
    else:
        return render(request, "home.html")

def contacto(request):
    try:
        context = {"id": request.session['id'], "session_key": request.session.session_key}
        return render(request, "contacto.html", context=context)
    except:
        return render(request, "contacto.html")

'''
    Retornar una lista con los puntos de una ruta por id
    Se retornan como una lista de diccionarios para que los pasen a JSON luego
'''
def puntos_de_ruta(id_ruta):
    # Conseguir los puntos de la ruta ordenados por el serial 
    registros_puntos = Punto.objects.filter(ruta_id=id_ruta).order_by("serial")
    puntos = []
    for punto in registros_puntos:
        puntos.append({
            "serial":punto.serial,
            "lat":punto.latitud,
            "lon":punto.longitud
        })
    return puntos

'''
    Retornar todas las rutas de una empresa serializadas a JSON
'''
def api_rutas_por_empresa(request, id):
    # Buscar todas las rutas por empresa 
    registros_rutas = Ruta.objects.select_related('empresa').filter(empresa_id=id)
    
    # Lista de objetos JSON de rutas
    rutas = []

    for registro in registros_rutas:
        # Conseguir los puntos de la ruta
        puntos = puntos_de_ruta(registro.id)
        
        # Llenar nuevo objeto json con datos
        obj = {
            "numero_ruta" : registro.numero_ruta,
            "nombre_empresa" : registro.empresa.nombre,
            "descripcion" : registro.descripcion,
            "precio" : registro.precio,
            "horario" : registro.horario,
            "duracion" : registro.duracion,
            "rampa" : registro.rampa,
            "puntos" : puntos
        }

        # Agregarlo a la lista 
        rutas.append(obj)

    response = {"rutas":rutas}
    
    return HttpResponse(json.dumps(response))

'''
    Retornar los puntos de una ruta serializadas a JSON
'''
def api_puntos_por_num_ruta(request, num_ruta):
    
    # Buscar ruta por el su numero
    ruta = Ruta.objects.filter(numero_ruta=num_ruta)[0]

    # Obtener los puntos usando el id 
    puntos = puntos_de_ruta(ruta.id)

    response = {"puntos":puntos}
    
    return HttpResponse(json.dumps(response))

'''
    Retorna si punto_eval está dentro del rectángulo marcado por 
    los dos puntos de referencia
    - Cada punto es una tupla (lat,lon)
'''
def esta_contenido(punto_ref1, punto_ref2, punto_eval):
    LAT = 0  #nombres para los indices en las tuplas
    LON = 1

    # Obtener la maxima longitud (Y)
    max_lon = max((punto_ref1[LON], punto_ref2[LON]))

    # Obtener la minima longitud (Y)
    min_lon = min((punto_ref1[LON], punto_ref2[LON]))

    # Obtener la maxima latitud (X)
    max_lat = max((punto_ref1[LAT], punto_ref2[LAT]))

    # Obtener la minima latitud (X)
    min_lat = min((punto_ref1[LAT], punto_ref2[LAT]))


    # print(f"minLat {min_lat}")
    # print(f"maxLat {max_lat}")
    # print(f"minLon {min_lon}")
    # print(f"maxLon {max_lon}")

    # Validar en rango 
    return (min_lat <= punto_eval[LAT] <= max_lat) and \
        (min_lon <= punto_eval[LON] <= max_lon)

'''
    Retornar las rutas que tienen destino final dentro de un rectangulo
    criterio = ["paradas","destinos"]
'''
def api_rutas_dentro(request, lat1, lon1, lat2, lon2, criterio):
    # Parsear los parametros a floats
    (lat1, lon1, lat2, lon2) = map(lambda x: float(x), (lat1, lon1, lat2, lon2))

    # Conseguir los rangos de latitud y longitud del area especificada
    ref1 = (lat1, lon1)
    ref2 = (lat2, lon2)

    if criterio=="paradas":
        # Obtener todos los puntos que son paradas
        paradas = Punto.objects.filter(esParada=True)

        ids_rutas = []
        # Filtrar los que están dentro del límite
        for parada in paradas:
            if(esta_contenido(ref1, ref2, (parada.latitud, parada.longitud))):
                ids_rutas.append(parada.ruta.id)

        rutas = []
        for id in ids_rutas:
            rutas.append(ruta_a_dicc(id))

        return HttpResponse(json.dumps({"rutas":rutas}))

    elif criterio == "destinos":
        # Obtener las ultimas paradas de las rutas
        destinos = Punto.objects.raw(
            "select *, max(serial) from app_punto group by ruta_id;")

        ids_rutas = []

        # Filtrar las que quedan dentro los rangos de búsqueda
        for dest in destinos:
            if(esta_contenido(ref1, ref2, (dest.latitud, dest.longitud))):
                ids_rutas.append(dest.ruta.id)

        rutas = []
        for id in ids_rutas:
            rutas.append(ruta_a_dicc(id))

        return HttpResponse(json.dumps({"rutas":rutas}))
    else:
        return HttpResponse(f"Criterio invalido: {criterio}")
    


'''
    Dado un id de ruta retornar un diccionario con todos los atributos simples
    de la ruta, sus puntos y el nombre de la empresa 
'''
def ruta_a_dicc(id_ruta):
    registro = Ruta.objects.filter(id=id_ruta)[0]

    # Conseguir los puntos de la ruta
    puntos = puntos_de_ruta(registro.id)

    # Llenar nuevo objeto json con datos
    return {
        "numero_ruta": registro.numero_ruta,
        "nombre_empresa": registro.empresa.nombre,
        "descripcion": registro.descripcion,
        "precio": registro.precio,
        "horario": registro.horario,
        "duracion": registro.duracion,
        "rampa": registro.rampa,
        "puntos": puntos
    }

def registrar_log(nombre_usuario, accion, tabla):
    log = Log()
    log.nombre_usuario = nombre_usuario
    log.accion = accion
    log.tabla = tabla
    log.save()

'''
    Página para buscar una ruta según diferentes criterios
'''
def buscar_rutas(request):
    return render(request, "buscar_rutas.html",{})
