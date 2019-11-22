from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from app.models import *

import json
import math

from datetime import datetime

from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.db.models.query import QuerySet

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
            ruta.empresa = Empresa.objects.filter(id=data["id_empresa"]).last()
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
            json_paradas = {}

            for parada in paradas:
                json_paradas[parada.serial] = {"latitud" : parada.latitud, "longitud" : parada.longitud, "esParada" : parada.esParada, "descripcion" : parada.descripcion}

            print(json_paradas)
            context = model_to_dict(ruta)
            context["action"] = "/ruta/editar/"+str(id)+"/"
            context["paradas"] = json.dumps(json_paradas)
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
            ruta.empresa = Empresa.objects.filter(id=data["id_empresa"]).last()
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
            return listar_rutas(request, meta=False)

        elif request.method == "GET":
            context = {"action":"/ruta/insertar/", "id": request.session['id'], "session_key": request.session.session_key}
            return render(request, "editar_crear_rutas.html", context=context)
    else:
        return render(request, "home.html")

def crear_paradas(data, ruta):

    # Parse string to json object
    json_paradas = json.loads(data['puntos'])
    print("Puntos string", data['puntos'])
    # Borrar paradas previamente asociadas
    Punto.objects.filter(ruta=ruta).delete()

    # Crear nuevas Paradas
    for serial in json_paradas.keys():
        parada = Punto()
        parada.ruta = ruta
        parada.serial = serial
        parada.latitud = json_paradas[serial]['latitud']
        parada.longitud = json_paradas[serial]['longitud']
        parada.esParada = json_paradas[serial]['esParada']
        parada.descripcion = json_paradas[serial]['descripcion']
        parada.save()

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
                    request.session.set_expiry(1200)
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
            "lon":punto.longitud,
            "esParada": punto.esParada
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
    context = {"id": request.session['id'], "session_key": request.session.session_key}
    return render(request, "buscar_rutas.html",context=context)


def api_ruta_por_id(request, id_ruta):
    id = int (id_ruta)
    ruta = Ruta.objects.filter(id=id)[0]

    resultado = {"rutas":[ruta_a_dicc(ruta.id)]}

    return HttpResponse(json.dumps(resultado))

'''
    Los logs se buscarán por fecha de inicio y fecha final
'''

def buscar_logs(request):
    if request.session.session_key:
        context = {"id": request.session['id'], "session_key": request.session.session_key}
        return render(request, "buscar_logs.html",context=context)
    else:
        return render(request, "home.html")

# convertir string -AAAA-MM-DD- a objeto datetime
def convertir_fecha(string):
    ANO = 0
    MES = 1
    DIA = 2
    campos = string.split("-")
    print(">>>",campos)
    return datetime(int(campos[ANO]), int(campos[MES]), int(campos[DIA]))

def api_buscar_logs(request, fecha_inicio, fecha_fin):
    print(f"{fecha_inicio} to {fecha_fin}")

    inicio = convertir_fecha(fecha_inicio)
    fin = convertir_fecha(fecha_fin)
    fin = fin.replace(hour=23) #validate all day

    logs = Log.objects.filter(hora__range=[inicio, fin])

    result = []
    for log in logs:
        result.append({
            "fecha":log.hora.strftime("%a %d %b %Y"),
            "usuario":log.nombre_usuario.nombre_usuario,
            "accion":log.accion,
            "tabla":log.tabla
        })
    return HttpResponse(json.dumps(result))

def api_parada_mas_cercana(request, usr_lat, usr_long, dest_lat, dest_long, rampa_required):

    # Parsear los parametros a floats
    (usr_lat, usr_long, dest_lat, dest_long) = map(lambda x: float(x), (usr_lat, usr_long, dest_lat, dest_long))

    # Obtener las ultimas paradas de cada ruta
    # TODO: optimizar esta consulta para que no traiga TODOS los puntos finales
    if (not bool(rampa_required)):
        print("NO OCUPA RAMPA")
        puntos_finales = Punto.objects.raw(
        "select *, max(serial) from app_punto group by ruta_id;")
    else:
        print("OCUPA RAMPA")
        puntos_finales = Punto.objects.raw(
        "select *, max(serial) from app_punto inner join app_ruta on ruta_id = app_ruta.id where app_ruta.rampa = 1 group by ruta_id;")

    print("Puntos finales ", len(puntos_finales))

    # Obtener los ids de las paradas finales mas cercas al destino
    ids_paradas_finales = get_n_nearest_points(len(puntos_finales), puntos_finales, dest_lat, dest_long)

    print("Ids: ", ids_paradas_finales)

    # Obtener las rutas que hacen match con los ids de las paradas cercanas
    rutas_cercanas = []
    for id in ids_paradas_finales:
        parada = Punto.objects.filter(id = id)[0]
        rutas_cercanas.append(parada.ruta)

    print("Rutas cercanas ", rutas_cercanas)

    # Obtener las paradas de cada ruta (no los puntos normales) y dejarlos en una lista
    paradas_rutas_cercanas = []
    for ruta in rutas_cercanas:
        paradas_ruta_actual = Punto.objects.filter(ruta = ruta, esParada = True)
        for parada in paradas_ruta_actual:
            paradas_rutas_cercanas.append(parada)

    print("Paradas de rutas ", paradas_rutas_cercanas)

    # Obtengo la parada mas cercana a mi posicion actual
    id_parada_mas_cercana = get_n_nearest_points(1, paradas_rutas_cercanas, usr_lat, usr_long)

    print("Id parada mas cercana: ", id_parada_mas_cercana)

    parada_mas_cercana = Punto.objects.filter(id = id_parada_mas_cercana[0])

    print("Parada mas cercana ", parada_mas_cercana)

    # Serializar las rutas cercanas a JSON
    resultado = []
    for ruta in rutas_cercanas:
        resultado.append(ruta_a_dicc(ruta.id))

    print("Resultado ", resultado)

    # Se retorna las rutas mas cercanas y las coordenadas de la parada a la cual debo ir
    return HttpResponse(json.dumps({"rutas":resultado, "pnt_lat" : parada_mas_cercana[0].latitud, \
                                    "pnt_lng" : parada_mas_cercana[0].longitud}))

'''
    Retorna los n puntos mas cercanos a (lat, long) en el mapa
'''
def get_n_nearest_points(n, puntos, dest_lat, dest_lon):

    final_dest_lat = abs(dest_lat)
    final_dest_lon = abs(dest_lon)
    final_distances = []

    i = 0
    print("Len puntos ", len(puntos))
    while(i < len(puntos)):

        latitud_actual = 0
        longitud_actual = 0
        punto_id = -1

        # Se verifica si el objeto es un punto literal o un QuerySet con un punto dentro
        if(isinstance(puntos[1], QuerySet)):
            latitud_actual = puntos[i][0].latitud
            longitud_actual = puntos[i][0].longitud
            punto_id = puntos[i][0].id
        else:
            latitud_actual = puntos[i].latitud
            longitud_actual = puntos[i].longitud
            punto_id = puntos[i].id

        # Formula Pitagoras
        cateto_a = abs(latitud_actual - final_dest_lat)
        cateto_b = abs(longitud_actual - final_dest_lon)
        point_distance = math.sqrt(cateto_a**2 + cateto_b**2)

        # Guardar elementos (id, distancia al destino) en la lista final
        final_distances.append((punto_id, point_distance))
        print("Append")
        i += 1

    # Retorna la distancia dentro de una tupla de final_distances
    def get_distance_in_tuple(tuple_element):
        return tuple_element[1]

    # Ordenar de manera ascendente y por distancia, no por id
    final_distances.sort(key = get_distance_in_tuple)
    print("Final distances: ", final_distances)
    # Obtener todos los ids de la lista de tuplas
    map_iterator = map(lambda tuple_element: tuple_element[0], final_distances)
    return list(map_iterator)[:n] # Convert it to list and return only the first n elements



def api_rutas_por_tiempo(request, minutos):
    # Filtrar las rutas que duran la mitad del tiempo o menos
    # porque sería viaje ida y vuelta

    rutas = []

    for ruta in Ruta.objects.all():
        durac = int(ruta.duracion)
        max_durac = int(minutos/2)+1
        if( durac in range(0, max_durac)):
            rutas.append(ruta_a_dicc(ruta.id))

    return HttpResponse(json.dumps({"rutas":rutas}))
