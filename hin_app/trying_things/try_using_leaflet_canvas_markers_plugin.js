// Here's the html imports:
//   <!-- try using canvas-markers plugin to fix slowness - not necessary nevermind-->
//   <script src="https://unpkg.com/leaflet-canvas-marker@0.2.0"></script>
//   <script src="../node_modules/leaflet-canvas-markers/leaflet-canvas-markers.js"></script>
//   <script src="https://unpkg.com/rbush@3.0.1/rbush.js"></script>
//   <script src="../node_modules/leaflet-markers-canvas/dist/leaflet-markers-canvas.js"></script>

// try using leafet-markers-canvas plugin -- it's better than leaflet-canvas-markers
var markersCanvas = new L.MarkersCanvas();
markersCanvas.addTo(map);
var icon = L.icon({ // need to specify an icon even if it's a circle
  iconUrl: "marker.png",
  iconSize: [2, 2],
  iconAnchor: [0, 0],
});
var fars_markers = [];


var marker = L.marker(
    [row.LATITUDE, row.LONGITUD],
    { icon }
)
.bindPopup(row.STATENAME)
.on({
    mouseover(e) {
    this.openPopup();
    },
    mouseout(e) {
    this.closePopup();
    },
});
fars_markers.push(marker);


markersCanvas.addMarkers(fars_markers);
console.log("fars_markers", fars_markers);
