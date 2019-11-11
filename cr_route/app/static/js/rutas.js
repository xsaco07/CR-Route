var startPoint = {
  latitude: 10.0551648,
  longitude: -84.3148551
};

var markers = [];
var coordenates = [];
var polylines = []
var mymap = L.map('map').setView([startPoint.latitude, startPoint.longitude], 16);
var p_group = L.layerGroup(polylines).addTo(mymap);
var stop_flag = false;

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

  if(!stop_flag){
    newMarker = L.marker(e.latlng);
  }
  else{
    newMarker = L.marker(e.latlng, {icon: greenIcon});
  }

  var lat = e.latlng.lat;
  var lng = e.latlng.lng;

  newMarker.addTo(mymap);

  newMarker.on('click',function(){

    remove_marker(this);

  });

  markers.push(newMarker);
  coordenates.push([lat, lng]);

  draw_path(coordenates);

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

// This function is called the page is loaded with the purpose of updating a route
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
  markers.map(function(marker) {
    console.log("Cleaning marker");
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
  });

});

mymap.on('click', onMapClick);
