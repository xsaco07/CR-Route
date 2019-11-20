var startPoint = {
  latitude: 10.0551648,
  longitude: -84.3148551
};

var markers = [];
var coordenates = [];
var polylines = []
var descriptions = [];
var mymap = L.map('map').setView([startPoint.latitude, startPoint.longitude], 16);
var p_group = L.layerGroup(polylines).addTo(mymap);
var stop_flag = false;
const stop_form = "input"

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  maxZoom: 19
}).addTo(mymap);

function onMapClick(e) {

  var greenIcon = new L.Icon({
    iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  });

  var newMarker = null;

  // Is a stop?
  if(!stop_flag){

    newMarker = L.marker(e.latlng);
    newMarker.addTo(mymap);

    // Add function on click event
    newMarker.on('click',function(){
      remove_marker(this);
    });

  }

  else{

    newMarker = L.marker(e.latlng, {icon: greenIcon});
    newMarker.addTo(mymap);

    // Always deploy the form when is added to the map
    deploy_stop_form(newMarker)

    newMarker.on('click', function() {
      deploy_stop_form(newMarker);
    });

  }

  var lat = e.latlng.lat;
  var lng = e.latlng.lng;

  // Save marker in array
  // The description is empty unless the user intentionally fills it
  markers.push(newMarker);
  // Save new coordenates in array
  coordenates.push([lat, lng]);

  draw_path(coordenates);

}

// Shows the delete and add description options to the stop marker
// Add event handlers to both buttons
function deploy_stop_form(marker) {

  // Bind html to popup to make an markers_function
  // Add a description or delete it
  var options_html = "<h6 class='text-center'>Agregando Parada</h6> \
  <input type='button' class='btn btn-success' value='Describir' id='desc-btn-option'> \
  <input type='button' class='btn btn-danger' value='Eliminar' id='delete-btn-option'>";

  marker.bindPopup(options_html).openPopup();

  // Bind html to popup to add a description
  var add_desc_html = "<h5>Agregue una descripción</h5> \
  <div class='form-group'> \
  <input class='form-control' id='desc-input' type='text'> \
  </div> \
  <div class='text-center'> \
  <input type='button' class='btn btn-success' value='Listo' class='text-center' id='desc-btn'> \
  </div>";

  $('#desc-btn-option').click(function() {

    marker.bindPopup(add_desc_html).openPopup();

    // Save the descripction when btn is pressed
    $("#desc-btn").click(function() {
      var current_stop_description = $("#desc-input").val();
      var desc_position = markers.indexOf(marker);
      descriptions[desc_position] = current_stop_description;
      marker.closePopup();
    });

  });

  $('#delete-btn-option').click(function() {
    remove_marker(marker);
  });

}

// Takes the attributes from coords and markers array and
// turns it to an json object.
// marker: object where the attributes are taken
// is_stop: true if stop_flag was true when it was added to the map
// is_stop: false if stop_flag was false when it was added to the map
function marker_to_json(marker) {

  // If the description is not set means that is not a stop
  var is_stop = false;
  var description = "";
  if(descriptions[markers.indexOf(marker)] != null){
    is_stop = true;
    description = descriptions[markers.indexOf(marker)];
  }

  var json_object = {
    "latitud" : marker.getLatLng().lat,
    "longitud" : marker.getLatLng().lng,
    "esParada" : is_stop,
    "descripcion" : description
  };

  return json_object;
}

function get_all_points_json() {
  var current_serial = 0;
  var points = {};
  for(var i = 0; i < markers.length; i++) {
    points[(current_serial++).toString()] = marker_to_json(markers[i]);
  }
  console.log(points);
  return points;
}

function remove_marker(marker) {
  polylines = [];
  p_group.remove();
  marker.remove();

  var marker_lat = marker.getLatLng().lat;
  var marker_lng = marker.getLatLng().lng;

  var i = markers.indexOf(marker);

  markers.splice(i, 1);
  coordenates.splice(i, 1);

  draw_path(coordenates);

}

// This function is called when the page is loaded with the purpose of updating a route
// It takes the points from DB and draws the path through out the map
function draw_loaded_path() {
  markers = [];
  var final_coords = []
  var paradas_coords = JSON.parse(paradas); // Parse string to array of floats

  for (var i = 0; i < paradas_coords.length; i++) {

    // Create the markers
    var newMarker = L.marker(paradas_coords[i]);
    newMarker.addTo(mymap);
    newMarker.on('click',function(){markers_function(this);});
    markers.push(newMarker);

    final_coords.push.apply(final_coords, [paradas_coords[i]]);

  }

  // Clean polyline
  polylines = [];
  p_group.remove();

  // Draw polyline
  draw_path(final_coords);

  // Clear coords array
  coordenates = [];
  // Set coordenates parsed from django view
  coordenates.push.apply(coordenates, final_coords);
}

function cleanMap() {
  polylines = [];
  coordenates = [];
  p_group.remove();
  p_group = L.layerGroup(polylines).addTo(mymap);

  // Apply remove function to every marker in array
  markers.map(function(marker) {
    marker.remove();
  });
}

// Takes an coordenates array and draws them on the map
function draw_path(coordenates) {
  polylines.push(L.polyline(coordenates, {color: 'red'}));
  p_group = L.layerGroup(polylines).addTo(mymap);
}

function setFlag(input) {
  if(input.checked) stop_flag = false;
  else stop_flag = true;
}

$(document).ready(function() {

  // Draw the path only when updating a route
  if(paradas) draw_loaded_path();

  var submit_button = $('button[type=submit]');

  submit_button.on('click', function() {
    var hidden_input = $('#puntos-ruta');
    hidden_input.val(coordenates.toString());
    console.log(get_all_points_json());
  });

});

mymap.on('click', onMapClick);
