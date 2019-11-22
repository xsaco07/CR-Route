var mapa;
var puntos_ref = []; // lista de los puntos de referencia para buscar
var polygon_area;
var destiny_coords = [];
var layer_group; // todos los elementos en el mapa

const FALSE = 0
const TRUE = 1

// Icono de la parada mas cerca a mi posicion
var closestStopIcon = new L.Icon({
  iconUrl: 'https://www.uv.es/uwm/imatges/GMaps/markers/red-marker.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

// Icono del destino al cual deseo ir
var destinyMarkerIcon = new L.Icon({
  iconUrl: 'https://icons-for-free.com/iconfiles/png/512/my+location+48px-131987943379423279.png',
  iconSize: [40, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

var greenIcon = new L.Icon({
  iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

// Dibuja un rectangulo marcado por los puntos_ref dentro del mapa
function dibujar_area(){
    if(puntos_ref.length == 2){
        var lats = [puntos_ref[0].lat, puntos_ref[1].lat];
        var lons = [puntos_ref[0].lng, puntos_ref[1].lng];
        var max_lat = Math.max(lats[0],lats[1]);
        var min_lat = Math.min(lats[0],lats[1]);
        var max_lon = Math.max(lons[0], lons[1]);
        var min_lon = Math.min(lons[0], lons[1]);

        polygon_area = L.polygon([
            [max_lat, min_lon],
            [max_lat, max_lon],
            [min_lat, max_lon],
            [min_lat, min_lon]
        ]);

        polygon_area.addTo(mapa);
    }else{
        console.log("Sin suficientes puntos");
    }
}

function limpiar_area(){
    if(polygon_area != undefined) polygon_area.remove();
    puntos_ref = [];
    actualizar_inputs();
    console.log("area limpiada");
}

// Copiar los valores de puntos refs a los inputs en la pagina
function actualizar_inputs(){

    if(puntos_ref.length == 0){
        $("#Punto1").val("");
        $("#Punto2").val("");
    }
    else if(puntos_ref.length==1){
        var punto_ref = puntos_ref[0];
        $("#Punto1").val(punto_ref.lat+","+punto_ref.lng);
    }
    else if(puntos_ref.length==2){
        var punto_ref = puntos_ref[1];
        $("#Punto2").val(punto_ref.lat+","+punto_ref.lng);
    }
}

function habilitar_seleccionar_area(){

    $("#limpiar").on("click",function(){
        limpiar_area();
    });

    mapa.on("click",function(e){
        // Habilitar click para agregar punto de destino
        if($("#criterio").val() == "parada_cercana" || $("#criterio").val() == "parada_cercana_rampa") {
          console.log("Destiny added");
          var destinyMarker = L.marker(e.latlng, {icon: destinyMarkerIcon});
          destiny_coords = [e.latlng.lat, e.latlng.lng];
          destinyMarker.addTo(mapa);
        }
        else {
          if(puntos_ref.length < 2){
              puntos_ref.push(e.latlng);
              console.log("punto agregado "+puntos_ref);

              actualizar_inputs();

              if(puntos_ref.length == 2){
                  dibujar_area();
              }
          }
          else console.log("refs llenos");
        }
    });
}

function configurar_mapa() {
    mapa = L.map('map').setView([51.505, -0.09], 13);
    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
            '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
            'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        id: 'mapbox.streets'
    }).addTo(mapa);

    center_map(mapa);
}

function getRandomColor(){
    const colores = ["green","red","blue","yellow","magenta","cyan","purple"];
    const i = Math.round(Math.random()*(colores.length-1));
    return colores[i];
}

function pedir_rutas(){
    // Ver qué criterio se está usando
    // y construir url según el criterio
    var criterio = $("#criterio").val();
    var api_url;
    if(criterio == "empresa"){
        var id_empresa = $("#combo_empresa").val();
        api_url = `/api/rutas_por_empresa/${id_empresa}/`
    }
    else if(criterio == "ruta"){
        var num_ruta = $("#num_ruta").val();
        api_url = `/api/ruta_por_id/${num_ruta}/`
    }
    else if(criterio == "destino"){
        coords1 = $("#Punto1").val();
        coords2 = $("#Punto2").val();
        api_url = `/api/rutas_dentro/${coords1}/${coords2}/destinos/`
    }
    else if(criterio == "paradas"){
        coords1 = $("#Punto1").val();
        coords2 = $("#Punto2").val();
        api_url = `/api/rutas_dentro/${coords1}/${coords2}/paradas/`
    }
    else if(criterio == "parada_cercana"){
        var usr_lat = MY_COORDS[0];
        var usr_long = MY_COORDS[1];
        var dest_lat = destiny_coords[0];
        var dest_long = destiny_coords[1];
        console.log(dest_lat, dest_long);
        api_url = `/api/parada_mas_cercana/${usr_lat},${usr_long}/${dest_lat},${dest_long}/${FALSE}`
    }
    else if(criterio == "parada_cercana_rampa"){
        var usr_lat = MY_COORDS[0];
        var usr_long = MY_COORDS[1];
        var dest_lat = destiny_coords[0];
        var dest_long = destiny_coords[1];
        console.log(dest_lat, dest_long);
        api_url = `/api/parada_mas_cercana/${usr_lat},${usr_long}/${dest_lat},${dest_long}/${TRUE}`
    }
    else{
        console.log(`criterio desconocido: ${criterio}`)
    }

    // Enviar peticion AJAX
    $.ajax({url:api_url})
    .done(function(data){
        var polylines = [];
        var marcadores = [];

        var obj_json = JSON.parse(data);

        obj_json.rutas.forEach(function(ruta){

            var coords = [];

            ruta.puntos.forEach(function(punto){

              coords.push([punto.lat, punto.lon]); // agregar el punto a la traza

              if(punto.esParada){

                  // Es el punto mas cercano?
                  console.log("Lat1 " + punto.lat + " " + "Lat2 " + obj_json.pnt_lat);
                  console.log("Lng1 " + punto.lon + " " + "Lng2 " + obj_json.pnt_lng);
                  if(punto.lat == obj_json.pnt_lat && punto.lon == obj_json.pnt_lng){
                    marcadores.push(L.marker([punto.lat, punto.lon], {icon : closestStopIcon}));
                  }
                  else marcadores.push(L.marker([punto.lat, punto.lon], {icon : greenIcon}));
              }
              else marcadores.push(L.marker([punto.lat, punto.lon]));

            });

            var line = L.polyline(coords, {color:getRandomColor()});
            line.bindTooltip(`Ruta #${ruta.numero_ruta} ‎${ruta.descripcion} ₡${ruta.precio}`).openTooltip();
            polylines.push(line);

            console.log(`ruta numero [${ruta.numero_ruta}] agregada al mapa`);
        });

        // Pintar rutas recibidas en el mapa
        if(layer_group == undefined){
            layer_group = L.layerGroup(polylines.concat(marcadores));
            layer_group.addTo(mapa);

        }else{
            polylines.concat(marcadores).forEach(function(layer){
                layer_group.addLayer(layer);
            });
        }

    });

}

function limpiar_mapa(){
    if(layer_group != undefined) layer_group.clearLayers();
}

$(document).ready(function () {
    // Configurar funcionamiento dinámico del formulario
    $("#criterio").on("change", criterio_cambiado);

    configurar_mapa();

    habilitar_seleccionar_area();

    // Prevenir que el botón buscar envíe el formulario
    // porque los datos se traerán por ajax para renderizar en el mapa
    $("form").submit(function(e){
        e.preventDefault(e);
    });

    $("#buscar").on("click", pedir_rutas);

    $("#limpiar_mapa").on("click", limpiar_mapa);


});

function criterio_cambiado() {
    // Limpiar la zona de campos variables
    $("#campos").empty();

    // Rellenar la zona según el criterio seleccionado
    switch (this.value) {
        case "empresa":
            form_por_empresa();
            break;
        case "ruta":
            form_por_ruta();
            break;
        case "destino":
            form_por_destino();
            break
        case "paradas":
            form_por_paradas();
            break;
    }
}

// Agrega un combo con las empresas
function form_por_empresa() {

    // Crear el combo
    var combo_empresa = document.createElement("select");
    $(combo_empresa).addClass("form-control");
    $(combo_empresa).attr("id","combo_empresa");
    var div = document.createElement("div");
    $(div).addClass("form-group");

    // Hacer la peticion para conseguir las empresas
    $.ajax({
        url: "/empresa/listar/meta/",
    }).done(function (data) {
        $(combo_empresa).html(data);
    });

    // Agregar el combo la página
    $("#campos").append(combo_empresa);
}

// Agrega un datalist con todas la rutas en su descripcion y empresa
function form_por_ruta() {

    // Crear la lista opciones
    var lista = $(document.createElement("datalist"));
    lista.attr("id", "lista_rutas");

    // Crear input y ponerle la referencia a su lista
    var input = $(document.createElement("input"));
    input.attr("list", "lista_rutas");
    input.attr("placeholder", "Buscar...")
    input.attr("id","num_ruta")
    input.append(lista); // agregar la lista dentro del input

    // Agregar el input a la página
    $("#campos").append(input);

    // Enviar petición para listar las rutas (opciones)
    $.ajax({
        url: "/ruta/listar/meta/"
    }).done(function (data) {
        // Deserializar la respuesta
        const rutas = JSON.parse(data);

        // Crear un <option> por cada ruta
        rutas.forEach(function (ruta) {
            var option = $(document.createElement("option"));
            // Lo que se mostrará en pantalla (nombre legible)
            option.html(`${ruta.descripcion} [${ruta.empresa}]`);
            // El valor que se enviará realmente
            option.attr("value", ruta.id);
            // Agregar la nueva opción a la lista ya existente
            $(lista).append(option);

        });

    });
}

// Agregar un mapa a la página para que el usuario pueda delimitar el
// área de búsqueda deseada
function form_por_destino() {
    var nombres = ["Punto1", "Punto2"];

    nombres.forEach(function(nombre){
        var div = $(document.createElement("div"));
        div.addClass("form-group");

        var label = $(document.createElement("label"));
        label.html(nombre);
        div.append(label)

        var input = $(document.createElement("input"));
        input.attr("type","text");
        input.prop("disabled",true);
        input.attr("id",nombre);
        input.addClass("form-control");

        div.append(input);

        $("#campos").append(div);
    });
}

// Agregar un mapa a la página para que el usuario pueda delimitar el
// área de búsqueda deseada
function form_por_paradas() {
    // Es la misma cosa
    form_por_destino();
}
