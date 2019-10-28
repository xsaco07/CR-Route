var startPoint = {
  latitude: 10.0551648,
  longitude: -84.3148551
};

var mymap = L.map('map').setView([startPoint.latitude, startPoint.longitude], 16);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  maxZoom: 19
}).addTo(mymap);

var markers = [];
var coordenates = [];
var polylines = []
var p_group;

function onMapClick(e) {

  var newMarker = L.marker(e.latlng);
  var lat = e.latlng.lat;
  var lng = e.latlng.lng;

  newMarker.addTo(mymap);

  newMarker.on('click',function(){

    polylines = [];
    p_group.remove();
    this.remove();

    var marker_lat = this.getLatLng().lat;
    var marker_lng = this.getLatLng().lng;

    var i = markers.indexOf(this);

    console.log("I: ", i);

    markers.splice(i, 1);
    coordenates.splice(i, 1);

    polylines.push(L.polyline(coordenates, {color: 'red'}));
    p_group = L.layerGroup(polylines).addTo(mymap);

  });

  markers.push(newMarker);
  coordenates.push([lat, lng]);

  console.log("Pushed: ", coordenates);
  polylines.push(L.polyline(coordenates, {color: 'red'}));
  p_group = L.layerGroup(polylines).addTo(mymap);

}

mymap.on('click', onMapClick);

$(document).ready(function() {
  var submit_button = $('button[type=submit]');
  submit_button.on('click', function() {
    var hidden_input = $('#puntos-ruta');
    hidden_input.val(coordenates,toString());
    console.log('coordenates loaded');
  });
});
