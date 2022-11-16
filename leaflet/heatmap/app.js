// ORIGINAL BASE MAP EXAMPLE
// var L = require('leaflet');
// var map = L.map('map', {
//   scrollWheelZoom: false
// });
// map.setView([47.70, 13.35], 7);
// var osm_mapnik = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
// 	maxZoom: 19,
// 	attribution: '&copy; OSM Mapnik <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
// }).addTo(map);


// ------------------------------------------
// HEATMAP EXAMPLE
var L = require('leaflet');

// Create the base Leaflet layer (the map itself)
let baseLayer = L.tileLayer(
    'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a>'
    }
)

// Configure and create the heatmap.js layer. Check out the heatmap.js Leaflet plugin docs for additional configuration options.
let cfg = {
    "radius": 40,
    "useLocalExtrema": true,
    valueField: 'price'
};
let heatmapLayer = new HeatmapOverlay(cfg);

var sale = require('./federal_hill_sales.json');

// Determine min/max (from JSON data exposed as variable in sales.js) for the heatmap.js plugin
let min = Math.min(...sale.map(sale => sale.value))
let max = Math.max(...sale.map(sale => sale.value))

// Create the overall Leaflet map using the two layers we created
let propertyHeatMap = new L.Map('map', {
    center: new L.LatLng(39.275, -76.613),
    zoom: 15,
    layers: [baseLayer, heatmapLayer]
})

// Add data (from JSON data exposed as variable in sales.js) to the heatmap.js layer
heatmapLayer.setData({
    min: min,
    max: max,
    data: sale
});