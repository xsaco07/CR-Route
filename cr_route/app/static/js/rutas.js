var startPoint = {
  latitude: 10.0551648,
  longitude: -84.3148551
};

var mymap = L.map('map').setView([startPoint.latitude, startPoint.longitude], 16);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  maxZoom: 19
}).addTo(mymap);

var marker = L.marker([startPoint.latitude, startPoint.longitude]).addTo(mymap);
var marker = L.marker([10.0515451, -84.3144467]).addTo(mymap);
var marker = L.marker([10.0472983, -84.315735]).addTo(mymap);

var trace = [
    [startPoint.latitude, startPoint.longitude],
    [10.0515451, -84.3144467],
    [10.0472983, -84.315735]
];

var polyline = L.polyline(trace, {color: 'red'}).addTo(mymap);
