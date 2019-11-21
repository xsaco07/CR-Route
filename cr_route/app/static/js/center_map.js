var map;

function center_map(map_object){
    map = map_object;

    // Get user location 
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(onRequestGranted, onRequestDenied);
    }
};

function onRequestGranted (location){
    var coords = [location.coords.latitude, location.coords.longitude];
    L.marker(coords).addTo(map);
    map.setView(coords, 13);
}
function onRequestDenied(error){
    alert("Error, couldn't get your location, sorry we can't locate you on the map");
}