
var L = require('leaflet');


// magnification with which the map will start
const zoom = 3;
// coordinates
const lat = 45.0;
const lng = -93.25;

const osmLink = '<a href="http://openstreetmap.org">OpenStreetMap</a>';
const cartoDB = '<a href="http://cartodb.com/attributions">CartoDB</a>';

const osmUrl = "http://tile.openstreetmap.org/{z}/{x}/{y}.png";
const osmAttrib = `&copy; ${osmLink} Contributors`;
const landUrl = "https://{s}.basemaps.cartocdn.com/rastertiles/dark_all/{z}/{x}/{y}.png";
const cartoAttrib = `&copy; ${osmLink} Contributors & ${cartoDB}`;

const osmMap = L.tileLayer(osmUrl, { attribution: osmAttrib });
const landMap = L.tileLayer(landUrl, { attribution: cartoAttrib });

// config map
let config = {
  layers: [osmMap],
  minZoom: 3,
  maxZoom: 18,
  preferCanvas: true, // helps to fix slowness by plotting points on a canvas rather than individual layers
  // fullscreenControl: true,
};


const pointsA = [
  [44.960020586193795,  -93.25083755493164, "point A1"],
  [44.95924616170657,   -93.251320352554325, "point A2"],
  [44.959511304688444,  -93.25270973682404, "point A3"],
  [44.96040500771883,   -93.252146472930908, "point A4"],
];

const pointsB = [
  [44.959314161892106,  -93.252055277824405, "point B1"],
  [44.95950144756943,   -93.25193726062775, "point B2"],
  [44.95966573260081,   -93.251829972267154, "point B3"],
  [44.9598333027065,    -93.251744141578678, "point B4"],
  [44.9599680154701,    -93.25164758205414, "point B5"],
  [44.96012572746442,   -93.251583209037784, "point B6"],
  [44.960276867580336,  -93.25143836975098, "point B7"],
  [44.96046414919644,   -93.251341810226444, "point B8"],
];

// calling map
const map = L.map("map", config).setView([lat, lng], zoom);

var baseLayers = {
  "OSM Mapnik": osmMap,
  CartoDB: landMap,
};

// L.control.layers(baseLayers).addTo(map);
L.control.layers(baseLayers, null, {collapsed:false}).addTo(map); // makes layer control not collapse, stay expanded


// Extended `LayerGroup` that makes it easy to do the same for all layers of its members
const pA = new L.FeatureGroup();
const pB = new L.FeatureGroup();
const fars_points = new L.FeatureGroup();
const mpo_boundaries = new L.FeatureGroup();
const county_boundaries = new L.FeatureGroup();
const state_boundaries = new L.FeatureGroup();
const census_boundaries = new L.FeatureGroup(); // TODO: implement

// adding markers to the layer pointsA
for (let i = 0; i < pointsA.length; i++) {
  // var marker = L.marker([pointsA[i][0], pointsA[i][1]]).bindPopup(pointsA[i][2]);
  var marker = L.circleMarker([pointsA[i][0], pointsA[i][1]], {radius: 10, color: '#FF00FF'}).bindPopup(pointsA[i][2]);
  pA.addLayer(marker);
}


// START OF CSV READING LILO
var FARS_renderer = L.canvas({ padding: 0.5 }); // helps to fix slowness by plotting points on a canvas rather than individual layers
d3.csv('https://raw.githubusercontent.com/Santos-Volpe-SCOPE/Santos-Volpe-SCOPE-Project/app-framework/FARS2020NationalCSV/accident.csv', function(data) {
  console.log("data.length", data.length);
  
  // for (var i = 0; i < 2000; i++) { 
  for (var i = 0; i < data.length; i++) {
    // console.log("index = ", i);
    // console.log(data[i].LATITUDE);
    // console.log(data[i].LONGITUD);

    var row = data[i];
      
    // ways to make markers:
    // var marker = L.marker([row.LATITUDE, row.LONGITUD], {});
    // var marker = L.circle( ... )
    // var marker = L.circleMarker([row.LATITUDE, row.LONGITUD], {opacity: 1, radius: 1, color: "red"}).bindPopup(row.STATENAME);
    // marker.addTo(map);

    // if (row.STATENAME == "California") { // | row.STATENAME == "Texas"){
    if (row.LATITUDENAME != "Not Available" & row.LONGITUDNAME != "Not Available" & row.LATITUDENAME != "Not Reported" & row.LONGITUDNAME != "Not Reported" & row.LATITUDENAME != "Reported as Unknown" & row.LONGITUDNAME != "Reported as Unknown"){
      // // renderer option helps to fix slowness by plotting points on a canvas rather than individual layers
      var marker = L.circleMarker([row.LATITUDE, row.LONGITUD], {radius: 1, opacity: 0.5, color: '#000000', renderer: FARS_renderer}).bindPopup(row.STATENAME); //.addTo(map);
      fars_points.addLayer(marker);
    }
    // }
  }
});

// var layerControl = L.control.layers(baseLayers, overlayMaps).addTo(map);
// layerControl.addOverlay(L.layerGroup(accident_markers), "FARS2020 Accidents");


// adding markers to the layer pointsB
for (let i = 0; i < pointsB.length; i++) {
  marker = L.marker([pointsB[i][0], pointsB[i][1]]).bindPopup(pointsB[i][2]);
  pB.addLayer(marker);
}


// centering a group of markers
map.on("layeradd layerremove", function () {
  // Create new empty bounds
  let bounds = new L.LatLngBounds();
  // Iterate the map's layers
  // // DO NOT UNCOMMENT SOMETHING IN HERE BREAKS AND MAKES THINGS SLOW
  // map.eachLayer(function (layer) {
  //   // Check if layer is a featuregroup
    // if (layer instanceof L.FeatureGroup) {
    //   // Extend bounds with group's bounds
    //   bounds.extend(layer.getBounds());
    // }
    // console.log("hi");
  // });

  // Check if bounds are valid (could be empty)
  if (bounds.isValid()) {
    // Valid, fit bounds
    map.flyToBounds(bounds);
  } else {
    // Invalid, fit world
    // map.fitWorld();
  }
});


L.Control.CustomButtons = L.Control.Layers.extend({
  onAdd: function () {
    this._initLayout();
    this._addMarker();
    this._removeMarker();
    this._update();
    return this._container;
  },
  _addMarker: function () {
    this.createButton("add", "add-button");
  },
  _removeMarker: function () {
    this.createButton("remove", "remove-button");
  },
  createButton: function (type, className) {
    const elements = this._container.getElementsByClassName(
      "leaflet-control-layers-list"
    );
    const button = L.DomUtil.create(
      "button",
      `btn-markers ${className}`,
      elements[0]
    );
    button.textContent = `${type} markers`;

    L.DomEvent.on(button, "click", function (e) {
      const checkbox = document.querySelectorAll(
        ".leaflet-control-layers-overlays input[type=checkbox]"
      );

      // Remove/add all layer from map when click on button
      [].slice.call(checkbox).map((el) => {
        el.checked = type === "add" ? false : true;
        el.click();
      });
    });
  },
});

// // one marker example
// coord = [52.22983, 21.011728];
// L.marker(coord).addTo(map).bindPopup("Center Warsaw\n" + coord.join());

// this was a text box on the bottom left of the screen:
// const markerPlace = document.querySelector(".marker-position");

// obtaining coordinates after clicking on the map
map.on("click", function (e) {
  // const markerPlace = document.querySelector(".marker-position");
  // markerPlace.textContent = e.latlng;
  console.log("Clicked on", e.latlng);
});


// on drag end
map.on("dragend", setRentacle);

// second option, by dragging the map
map.on("dragstart", updateInfo);

// on zoom end
map.on("zoomend", setRentacle);

// update info about bounds when site loaded
document.addEventListener("DOMContentLoaded", function () {
  const bounds = map.getBounds();
  updateInfo(bounds._northEast, bounds._southWest);
});

// set rentacle function
function setRentacle() {
  const bounds = map.getBounds();

  // update info about bounds
  updateInfo(bounds._northEast, bounds._southWest);

  // // set rentacle
  // L.rectangle(bounds, {
  //   color: randomColor(),
  //   weight: 20,
  //   fillOpacity: 0.1,
  // }).addTo(map);

  // set map
  map.fitBounds(bounds);
}

// generate random color
function randomColor() {
  return `#${Math.floor(Math.random() * 16777215).toString(16)}`;
}

function updateInfo(north, south) {
  // console.log("moving the map", north, south);
  // markerPlace.textContent =
  var textContent = 
    south === undefined
      ? "We are moving the map..."
      : `SouthWest: ${north}, NorthEast: ${south}`;
    console.log(textContent);
}


// ------------------------------------------------------------------------------------
// HEATMAP EXAMPLE
var L = require('leaflet');

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

// Add data (from JSON data exposed as variable in sales.js) to the heatmap.js layer
heatmapLayer.setData({
    min: min,
    max: max,
    data: sale
});


// -----------------------------------------------------------------------------------------
// LOAD GEOJSON OF MPOS

function setMposToMap(geojson) {
  const feature = L.geoJSON(geojson, {
    style: function (feature) {
      return {
        color: "blue",
        weight: 1,
      };
    },
    // pointToLayer: (feature, latlng) => {
      // if (feature.properties.type === "circle") {
      //   return new L.circle(latlng, {
      //     radius: feature.properties.radius,
      //   });
      // } else if (feature.properties.type === "circlemarker") {
      //   return new L.circleMarker(latlng, {
      //     radius: 10,
      //   });
      // } else {
      //   return new L.Marker(latlng);
      // }
    // },
    onEachFeature: function (feature, layer) {
      // drawnItems.addLayer(layer);
      // const coordinates = feature.geometry.coordinates.toString();
      // const result = coordinates.match(/[^,]+,[^,]+/g);
      // layer.bindPopup(
      //   "<span>Coordinates:<br>" + result.join("<br>") + "</span>"
      // );

      const mpo_name = feature.properties.MPO_NAME.toString();
      layer.bindPopup(
        "<span>MPO Name:<br>" + mpo_name + "</span>"
      );
    },
  }); //.addTo(map);
  console.log("feature", feature);
  mpo_boundaries.addLayer(feature);
  // map.flyToBounds(feature.getBounds());
}

d3.json('https://raw.githubusercontent.com/Santos-Volpe-SCOPE/Santos-Volpe-SCOPE-Project/app-framework/hin_app/mpo_data/mpo_boundaries.geojson', function(data) {
  const geojson = data;
  setMposToMap(geojson);
  console.log("mpo boundaries loaded");
});


// -----------------------------------------------------------------------------------------
// LOAD GEOJSON OF COUNTIES

function setCountiesToMap(geojson) {
  const feature = L.geoJSON(geojson, {
    style: function (feature) {
      return {
        color: "green",
        weight: 1,
      };
    },
    onEachFeature: function (feature, layer) {
      const county_name = feature.properties.NAME.toString();
      layer.bindPopup(
        "<span>County Name:<br>" + county_name + "</span>"
      );
    },
  }); //.addTo(map);
  console.log("feature", feature);
  county_boundaries.addLayer(feature);
  // map.flyToBounds(feature.getBounds());
}

d3.json('https://raw.githubusercontent.com/Santos-Volpe-SCOPE/Santos-Volpe-SCOPE-Project/app-framework/hin_app/county_data/county.geojson', function(data) {
  const geojson = data;
  setCountiesToMap(geojson);
  console.log("county boundaries loaded");
});


// -----------------------------------------------------------------------------------------
// LOAD GEOJSON OF STATES

function setStatesToMap(geojson) {
  const feature = L.geoJSON(geojson, {
    style: function (feature) {
      return {
        color: "red",
        weight: 1,
        opacity: 0.8,
        clickable: true
      };
    },
    onEachFeature: function (feature, layer) {
      const state_name = feature.properties.NAME.toString();
      layer.bindPopup(
        "<span>State Name:<br>" + state_name + "</span>"
      );

      layer.on('mouseover', function () {
        this.setStyle({
          'fillColor': '#0000ff'
        });
        this.openPopup();
      });
      
      layer.on('mouseout', function () {
        this.setStyle({
          'fillColor': '#ff0000'
        });
        this.closePopup(); 
      });

      layer.on('click', function (event) {
        map.fitBounds(this.getBounds());
        state_boundaries.removeLayer(feature)
      });


    },
  }); //.addTo(map);
  console.log("feature", feature);
  state_boundaries.addLayer(feature);
  // map.flyToBounds(feature.getBounds());
}


d3.json('https://raw.githubusercontent.com/Santos-Volpe-SCOPE/Santos-Volpe-SCOPE-Project/app-framework/hin_app/state_data/states.geojson', function(data) {
  const geojson = data;
  setStatesToMap(geojson);
  console.log("state boundaries loaded");
});


// -----------------------------------------------------------------------------------------
// ADD OVERLAYS ONTO MAP ON THE CUSTOM BUTTONS CONTROL PANEL

// object with layers
const overlayMaps = {
  "Circle Example": pA,
  "Pin Example": pB,
  "FARS 2020 Crashes": fars_points,
  "MPO Boundaries": mpo_boundaries,
  //"County Boundaries": county_boundaries,
  "State Boundaries": state_boundaries,
  "Example Heatmap": heatmapLayer,
};

// Trying to bring fars to back / bring heatmap to front:
// fars_points.bringToBack();

var custom_buttons_control = new L.Control.CustomButtons(null, overlayMaps, { collapsed: false }).addTo(map);


// -----------------------------------------------------------------------------------------
// TRIED TO LOAD GEOJSON FASTER. NOT REALLY WORKING

// var myStyle = {
//   "color": "#ff7800",
//   "weight": 5,
//   "opacity": 0.65
// };
// var geojsonMarkerOptions = {
//   radius: 8,
//   fillColor: "#ff7800",
//   color: "#000",
//   weight: 1,
//   opacity: 1,
//   fillOpacity: 0.8
// };

// d3.json('https://raw.githubusercontent.com/Santos-Volpe-SCOPE/Santos-Volpe-SCOPE-Project/app-framework/hin_app/mpo_data/mpo_boundaries.geojson', function(data) {
//   const geojsonFeature = data;
//   // setGeojsonToMap(geojson);
//   var myLayer = L.geoJSON().addTo(map);
//   myLayer.addData(geojsonFeature, {
//       style: myStyle,
//       onEachFeature: onEachFeature
//     });
//   console.log("mpo boundaries loaded");

//   function onEachFeature(feature, layer) {
//     layer.bindPopup(feature.properties.MPO_NAME);
//   }
// });


// ----------------------------------------------------------------------------------------------------
// sidebar

const menuItems = document.querySelectorAll(".menu-item");
const sidebar = document.querySelector(".sidebar");
const buttonClose = document.querySelector(".close-button");

menuItems.forEach((item) => {
  item.addEventListener("click", (e) => {
    const target = e.target;

    if (
      target.classList.contains("active-item") ||
      !document.querySelector(".active-sidebar")
    ) {
      document.body.classList.toggle("active-sidebar");
    }

    // show content
    showContent(target.dataset.item);
    // add active class to menu item
    addRemoveActiveItem(target, "active-item");
  });
});

// close sidebar when click on close button
buttonClose.addEventListener("click", () => {
  closeSidebar();
});

// remove active class from menu item and content
function addRemoveActiveItem(target, className) {
  const element = document.querySelector(`.${className}`);
  target.classList.add(className);
  if (!element) return;
  element.classList.remove(className);
}

// show specific content
function showContent(dataContent) {
  const idItem = document.querySelector(`#${dataContent}`);
  addRemoveActiveItem(idItem, "active-content");
}

// --------------------------------------------------
// close when click esc
document.addEventListener("keydown", function (event) {
  if (event.key === "Escape") {
    closeSidebar();
  }
});

// close sidebar when click outside
document.addEventListener("click", (e) => {
  if (!e.target.closest(".sidebar")) {
    closeSidebar();
  }
});

// --------------------------------------------------
// close sidebar

function closeSidebar() {
  document.body.classList.remove("active-sidebar");
  const element = document.querySelector(".active-item");
  const activeContent = document.querySelector(".active-content");
  if (!element) return;
  element.classList.remove("active-item");
  activeContent.classList.remove("active-content");
}


// ----------------------------------------------------------------------------------------------------
// SHAPEFILE UPLOAD AND DRAW MENUS

// // --------------------------------------------------
// // Nofiflix options

// Notiflix.Notify.init({
//   width: "280px",
//   position: "right-bottom",
//   distance: "10px",
// });

// // --------------------------------------------------
// // add buttons to map

// const customControl = L.Control.extend({
//   // button position
//   options: {
//     position: "topright",
//   },

//   // method
//   onAdd: function () {
//     const array = [
//       {
//         title: "export features geojson",
//         html: "<svg class='icon-geojson'><use xlink:href='#icon-export'></use></svg>",
//         className: "export link-button leaflet-bar",
//       },
//       {
//         title: "save geojson",
//         html: "<svg class='icon-geojson'><use xlink:href='#icon-add'></use></svg>",
//         className: "save link-button leaflet-bar",
//       },
//       {
//         title: "remove geojson",
//         html: "<svg class='icon-geojson'><use xlink:href='#icon-remove'></use></svg>",
//         className: "remove link-button leaflet-bar",
//       },
//       {
//         title: "load gejson from file",
//         html: "<input type='file' id='geojson' class='geojson' accept='text/plain, text/json, .geojson' onchange='openFile(event)' /><label for='geojson'><svg class='icon-geojson'><use xlink:href='#icon-import'></use></svg></label>",
//         className: "load link-button leaflet-bar",
//       },
//     ];

//     const container = L.DomUtil.create(
//       "div",
//       "leaflet-control leaflet-action-button"
//     );

//     array.forEach((item) => {
//       const button = L.DomUtil.create("a");
//       button.href = "#";
//       button.setAttribute("role", "button");

//       button.title = item.title;
//       button.innerHTML = item.html;
//       button.className += item.className;

//       // add buttons to container;
//       container.appendChild(button);
//     });

//     return container;
//   },
// });
// map.addControl(new customControl());

// // Drow polygon, circle, rectangle, polyline
// // --------------------------------------------------

// let drawnItems = L.featureGroup().addTo(map);

// map.addControl(
//   new L.Control.Draw({
//     edit: {
//       featureGroup: drawnItems,
//       poly: {
//         allowIntersection: false,
//       },
//     },
//     draw: {
//       polygon: {
//         allowIntersection: false,
//         showArea: true,
//       },
//     },
//   })
// );

// map.on(L.Draw.Event.CREATED, function (event) {
//   let layer = event.layer;
//   let feature = (layer.feature = layer.feature || {});
//   let type = event.layerType;

//   feature.type = feature.type || "Feature";
//   let props = (feature.properties = feature.properties || {});

//   props.type = type;

//   if (type === "circle") {
//     props.radius = layer.getRadius();
//   }

//   drawnItems.addLayer(layer);
// });

// // --------------------------------------------------
// // save geojson to file

// const exportJSON = document.querySelector(".export");

// exportJSON.addEventListener("click", () => {
//   // Extract GeoJson from featureGroup
//   const data = drawnItems.toGeoJSON();

//   if (data.features.length === 0) {
//     Notiflix.Notify.failure("You must have some data to save a geojson file");
//     return;
//   } else {
//     Notiflix.Notify.info("You can save the data to a geojson");
//   }

//   // Stringify the GeoJson
//   const convertedData =
//     "text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(data));

//   exportJSON.setAttribute("href", "data:" + convertedData);
//   exportJSON.setAttribute("download", "data.geojson");
// });

// // --------------------------------------------------
// // save geojson to localstorage
// const saveJSON = document.querySelector(".save");

// saveJSON.addEventListener("click", (e) => {
//   e.preventDefault();

//   const data = drawnItems.toGeoJSON();

//   if (data.features.length === 0) {
//     Notiflix.Notify.failure("You must have some data to save it");
//     return;
//   } else {
//     Notiflix.Notify.success("The data has been saved to localstorage");
//   }

//   localStorage.setItem("geojson", JSON.stringify(data));
// });

// // --------------------------------------------------
// // remove gojson from localstorage

// const removeJSON = document.querySelector(".remove");

// removeJSON.addEventListener("click", (e) => {
//   e.preventDefault();
//   localStorage.removeItem("geojson");

//   Notiflix.Notify.info("All layers have been deleted");

//   drawnItems.eachLayer(function (layer) {
//     drawnItems.removeLayer(layer);
//   });
// });

// // --------------------------------------------------
// // load geojson from localstorage

// const geojsonFromLocalStorage = JSON.parse(localStorage.getItem("geojson"));

// function setGeojsonToMap(geojson) {
//   const feature = L.geoJSON(geojson, {
//     style: function (feature) {
//       return {
//         color: "red",
//         weight: 1,
//       };
//     },
//     pointToLayer: (feature, latlng) => {
//       if (feature.properties.type === "circle") {
//         return new L.circle(latlng, {
//           radius: feature.properties.radius,
//         });
//       } else if (feature.properties.type === "circlemarker") {
//         return new L.circleMarker(latlng, {
//           radius: 10,
//         });
//       } else {
//         return new L.Marker(latlng);
//       }
//     },
//     onEachFeature: function (feature, layer) {
//       drawnItems.addLayer(layer);
//       const coordinates = feature.geometry.coordinates.toString();
//       const result = coordinates.match(/[^,]+,[^,]+/g);

//       layer.bindPopup(
//         "<span>Coordinates:<br>" + result.join("<br>") + "</span>"
//       );
//     },
//   }).addTo(map);

//   map.flyToBounds(feature.getBounds());
// }

// if (geojsonFromLocalStorage) {
//   setGeojsonToMap(geojsonFromLocalStorage);
// }

// // --------------------------------------------------
// // get geojson from file

// function openFile(event) {
//   const input = event.target;

//   const reader = new FileReader();
//   reader.onload = function () {
//     const result = reader.result;
//     const geojson = JSON.parse(result);

//     Notiflix.Notify.info("The data has been loaded from the file");

//     setGeojsonToMap(geojson);
//   };
//   reader.readAsText(input.files[0]);
// }
