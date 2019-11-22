var map;
var MY_COORDS = null;

// Icono de mi position actual en el mapa;
var myPosition = new L.Icon({
  iconUrl: 'https://cdn0.iconfinder.com/data/icons/location-9/54/my-pin-512.png',
  iconSize: [25, 41],
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
    map.setView(MY_COORDS, 13);
}
function onRequestDenied(error){
    alert("Error, couldn't get your location, sorry we can't locate you on the map");
}
