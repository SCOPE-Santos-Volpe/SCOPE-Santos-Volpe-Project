var map = L.map('map',
    {
        center:[11.47,8.20],
        zoom: 10
    });
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png').addTo(map);
    //var shpfile = new L.Shapefile('state_shp.zip');
    var shpfile = new L.Shapefile('./state_shp.zip');

      shpfile.addTo(map);

      var overlayMaps = {
            "TestShapefile": shpfile
        };

      L.control.layers(overlayMaps).addTo(map);
      
    shpfile.addTo(map);
    shpfile.once("data:loaded", function() {
        console.log("finished loaded shapefile");
    });
