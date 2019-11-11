var startPoint = {
  latitude: 10.0551648,
  longitude: -84.3148551
};

var markers = [];
var coordenates = [];
var polylines = []
var mymap = L.map('map').setView([startPoint.latitude, startPoint.longitude], 16);
var p_group = L.layerGroup(polylines).addTo(mymap);


L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  maxZoom: 19
}).addTo(mymap);

function onMapClick(e) {

  var newMarker = L.marker(e.latlng);
  var lat = e.latlng.lat;
  var lng = e.latlng.lng;

  newMarker.addTo(mymap);

  newMarker.on('click',function(){

    markers_function(this);

  });

  markers.push(newMarker);
  coordenates.push([lat, lng]);

  polylines.push(L.polyline(coordenates, {color: 'red'}));
  p_group = L.layerGroup(polylines).addTo(mymap);

}

function markers_function(marker) {
  polylines = [];
  p_group.remove();
  marker.remove();

  var marker_lat = marker.getLatLng().lat;
  var marker_lng = marker.getLatLng().lng;

  var i = markers.indexOf(marker);

  markers.splice(i, 1);
  coordenates.splice(i, 1);

  polylines.push(L.polyline(coordenates, {color: 'red'}));
  p_group = L.layerGroup(polylines).addTo(mymap);
}

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
  polylines.push(L.polyline(final_coords, {color: 'red'}));
  p_group = L.layerGroup(polylines).addTo(mymap);

  // Clear coords array
  coordenates = [];
  coordenates.push.apply(coordenates, final_coords);
}

function cleanMap() {
  console.log("Cleaning");
  polylines = [];
  coordenates = [];
  p_group.remove();
  p_group = L.layerGroup(polylines).addTo(mymap);
  markers.map(function(marker) {
    console.log("Cleaning marker");
    marker.remove();
  });
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
