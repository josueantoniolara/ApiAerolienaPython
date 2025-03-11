// Inicialización del mapa
var map = L.map("map", {
    center: [20.66682, -103.39215],
    zoom: 7,
    zoomControl: true,
    preferCanvas: false
});

// Capa base de OpenStreetMap
var baseLayer = L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    minZoom: 0,
    maxZoom: 19,
    maxNativeZoom: 19,
    noWrap: false,
    attribution: "&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors",
    subdomains: "abc",
    detectRetina: false,
    tms: false,
    opacity: 1
}).addTo(map);

// Capas de OpenWeatherMap
var lluvia = L.tileLayer("http://tile.openweathermap.org/map/precipitation_new/{z}/{x}/{y}.png?appid=0fca9e7d1796d9188a59015215bac279", {
    minZoom: 0,
    maxZoom: 18,
    maxNativeZoom: 18,
    noWrap: false,
    attribution: "OpenWeatherMap",
    subdomains: "abc",
    detectRetina: false,
    tms: false,
    opacity: 1
});

var nubes = L.tileLayer("http://tile.openweathermap.org/map/clouds_new/{z}/{x}/{y}.png?appid=0fca9e7d1796d9188a59015215bac279", {
    minZoom: 0,
    maxZoom: 18,
    maxNativeZoom: 18,
    noWrap: false,
    attribution: "OpenWeatherMap",
    subdomains: "abc",
    detectRetina: false,
    tms: false,
    opacity: 1
});

var temperatura = L.tileLayer("http://tile.openweathermap.org/map/temp_new/{z}/{x}/{y}.png?appid=0fca9e7d1796d9188a59015215bac279", {
    minZoom: 0,
    maxZoom: 18,
    maxNativeZoom: 18,
    noWrap: false,
    attribution: "OpenWeatherMap",
    subdomains: "abc",
    detectRetina: false,
    tms: false,
    opacity: 1
});

// Control de capas
L.control.layers(
    { "OpenStreetMap": baseLayer },
    { "Lluvia": lluvia, "Nubes": nubes, "Temperatura": temperatura },
    { position: "topright", collapsed: true, autoZIndex: true }
).addTo(map);
