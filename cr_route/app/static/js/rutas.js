var startPoint = {
  latitude: 10.0551648,
  longitude: -84.3148551
};

let markers = [];
let coordenates = [];
let polylines = [];
let descriptions = [];
var mymap = L.map('map').setView([startPoint.latitude, startPoint.longitude], 16);
var p_group = L.layerGroup(polylines).addTo(mymap);
var stop_flag = false;
const stop_form = "input"

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  maxZoom: 19
}).addTo(mymap);

var greenIcon = new L.Icon({
  iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

function onMapClick(e) {

  let newMarker = null;

  // Is a stop?
  if(!stop_flag){

    newMarker = L.marker(e.latlng);
    newMarker.addTo(mymap);

    var lat = e.latlng.lat;
    var lng = e.latlng.lng;

    // Save marker in array
    markers.push(newMarker);

    // Add function on click event
    newMarker.on('click',function(){
      remove_marker(this);
    });

  }

  else{

    newMarker = L.marker(e.latlng, {icon: greenIcon});
    newMarker.addTo(mymap);

    var lat = e.latlng.lat;
    var lng = e.latlng.lng;

    // Save marker in array
    markers.push(newMarker);

    // Always deploy the form when is added to the map
    deploy_stop_form(newMarker, "")

    newMarker.on('click', function() {
      deploy_stop_form(newMarker, "");
    });

  }

  // Save new coordenates in array
  coordenates.push([lat, lng]);

  draw_path(coordenates);

}

// Shows the delete and add description options to the stop marker
// Add event handlers to both buttons
// The description param is shown whe user is editing the route
function deploy_stop_form(marker, description) {
  console.log(markers.indexOf(marker));
  // Delete elements if they already exists in DOM
  if($('#desc-btn-option') != null) $('#desc-btn-option').remove();
  if($('#delete-btn-option') != null) $('#delete-btn-option').remove();

  // Bind html to popup to make an markers_function
  // Add a description or delete it
  var options_html = "<h5 class='text-center'>Agregando Parada</h5> \
  <input type='button' class='btn btn-success' value='Describir' id='desc-btn-option'> \
  <input type='button' class='btn btn-danger' value='Eliminar' id='delete-btn-option'>";

  marker.bindPopup(options_html).openPopup();

  // Delete elements if they already exists in DOM
  if($('#desc-btn-option') != null) $('#desc-input').remove();
  if($('#delete-btn-option') != null) $('#desc-btn').remove();

  // Bind html to popup to add a description
  var add_desc_html = "<h5>Agregue una descripción</h5> \
  <div class='form-group'> \
  <input class='form-control' id='desc-input' type='text'> \
  </div> \
  <div class='text-center'> \
  <input type='button' class='btn btn-success' value='Listo' class='text-center' id='desc-btn'> \
  </div>";

  // Guardar descripcion del punto siembre ( no requerir clickear describir)
  var desc_position = markers.indexOf(marker);
  descriptions[desc_position] = description;
  console.log("DESCS",descriptions);

  $('#desc-btn-option').click(function() {

    marker.bindPopup(add_desc_html).openPopup();

    // Set description to input field
    $("#desc-input").val(description);

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

  var is_stop = false;
  var description = "";

  // If the description is not set means that is not a stop
  if(descriptions[markers.indexOf(marker)] != undefined){
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
  return points;
}

function remove_marker(marker) {
  console.log("Marker removed");
  polylines = [];
  p_group.remove();
  marker.remove();

  var marker_lat = marker.getLatLng().lat;
  var marker_lng = marker.getLatLng().lng;

  var i = markers.indexOf(marker);

  markers.splice(i, 1);
  coordenates.splice(i, 1);
  descriptions.splice(i, 1);
  draw_path(coordenates);

}

// This function is called when the page is loaded with the purpose of updating a route
// It takes the points from DB and draws the path through out the map
function draw_loaded_path() {
  markers = [];
  descriptions = [];
  var final_coords = []
  let json_paradas = JSON.parse(paradas); // Parse json string to js object

  console.log(json_paradas);

  for (let i = 0; i < Object.keys(json_paradas).length; i++) {

    let newMarker = null;
    let description = json_paradas[i].descripcion;
    var current_coords = [json_paradas[i].latitud, json_paradas[i].longitud];

    // Create the markers
    // Use green icon if point is a stop
    if(json_paradas[i].esParada) {

      newMarker = L.marker(current_coords, {icon: greenIcon});
      markers.push(newMarker);

      newMarker.on('click', function() {
        deploy_stop_form(newMarker, description);
      });

      // Save description from json into descr array always
      var desc_position = markers.indexOf(newMarker);
      descriptions[desc_position] = description;

    }
    else {
      newMarker = L.marker(current_coords);
      newMarker.on('click',function(){remove_marker(this);});
      markers.push(newMarker);
    }

    newMarker.addTo(mymap);

    final_coords.push.apply(final_coords, [current_coords]);

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

  console.log("Cleaning");

  polylines = [];
  coordenates = [];
  descriptions = [];

  p_group.remove();
  p_group = L.layerGroup(polylines).addTo(mymap);

  // Apply remove function to every marker in array
  markers.map(function(marker) {
    marker.remove();
  });

  // Empty the array
  markers = [];

  console.log("Markers: " + markers);
}

// Takes a coordenates array and draws them on the map
function draw_path(coordenates) {
  polylines.push(L.polyline([coordenates], {color: 'red'}));
  p_group = L.layerGroup(polylines).addTo(mymap);
}

function setFlag(input) {
  if(input.checked) stop_flag = false;
  else stop_flag = true;
}

$(document).ready(function() {

  center_map(mymap);

  // Draw the path only when updating a route
  if(paradas) draw_loaded_path();

  var submit_button = $('button[type=submit]');

  submit_button.on('click', function() {
    var hidden_input = $('#puntos-ruta');
    hidden_input.val(JSON.stringify(get_all_points_json()));
  });

});

mymap.on('click', onMapClick);
