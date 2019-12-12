var map;
var MY_COORDS = null;

// Icono de mi position actual en el mapa;
var myPosition = new L.Icon({
  // iconUrl: 'https://cdn4.iconfinder.com/data/icons/pictype-free-vector-icons/16/location-alt-512.png',
  // iconUrl: 'https://icon-library.net/images/current-location-icon-png/current-location-icon-png-12.jpg',
  iconUrl: 'https://png.pngtree.com/svg/20170117/coordinate_646457.png',
  iconSize: [60, 60],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

function center_map(map_object){
    map = map_object;

    // Get user location
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(onRequestGranted, onRequestDenied);
    }
};

function onRequestGranted (location){
    MY_COORDS = [location.coords.latitude, location.coords.longitude];
    L.marker(MY_COORDS, {icon: myPosition}).addTo(map);

    $(document).ready(function() {

      $('[data-toggle="tooltip"]').tooltip();

      $('.leaflet-marker-icon').hover(function() {
        $(this).attr('data-toggle', 'tooltip');
        $(this).attr('data-placement', 'bottom');
        $(this).attr('title', 'Mi posición');
      });

    });

    map.setView(MY_COORDS, 14);
}
function onRequestDenied(error){
    alert("Error, no he podido localizarte, lo siento, no podemos localizarte en el mapa");
}
