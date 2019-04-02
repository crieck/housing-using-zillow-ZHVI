// init variables
var geojson_data = "static/js/mn-county-bounds.geojson";

const TWIN_CITIES_COORDINATES = [44.9833, -93.2667];

var colors= ['aqua', 'black', 'blue', 'fuchsia', 'gray', 'green',
'lime', 'maroon', 'navy', 'olive', 'orange', 'purple', 'red',
'silver', 'teal', 'white', 'yellow'];

// init map object
var map = L.map("map", {
  center: TWIN_CITIES_COORDINATES,
  zoom: 15
});

// init tile layer
L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.light",
  accessToken: MAPBOX_API_KEY
}).addTo(map);

// Function creates random colors, will be applied to leaflet features
function chooseColor(COUNTY_NAM) {
  Array.prototype.getRandom = function(cut){
    var i = Math.floor(Math.random()*this.length);
    if(cut && i in this){
        return this.splice(i, 1)[0];
    }
    return this[i];
  }
  return colors.getRandom();
}

// Grabbing our GeoJSON data..
d3.json(geojson_data, function(data) {
  // Creating a geoJSON layer with the retrieved data
  L.geoJson(data, {
    // Style each feature (in this case a COUNTY_NAM)
    style: function(feature) {
      return {
        color: "white",
        // Call the chooseColor function to decide which color to color our COUNTY_NAM (color based on COUNTY_NAM)
        fillColor: chooseColor(feature.properties.COUNTY_NAM),
        fillOpacity: 0.5,
        weight: 1.5
      };
    },
    // Called on each feature
    onEachFeature: function(feature, layer) {
      // Set mouse events to change map styling
      layer.on({
        // When a user's mouse touches a map feature, the mouseover event calls this function, that feature's opacity changes to 90% so that it stands out
        mouseover: function(event) {
          layer = event.target;
          layer.setStyle({
            fillOpacity: 0.9
          });
        },
        // When the cursor no longer hovers over a map feature - when the mouseout event occurs - the feature's opacity reverts back to 50%
        mouseout: function(event) {
          layer = event.target;
          layer.setStyle({
            fillOpacity: 0.5
          });
        },
        // When a feature (COUNTY_NAM) is clicked, it is enlarged to fit the screen
        click: function(event) {
          map.fitBounds(event.target.getBounds());
        }
      });
      // Giving each feature a pop-up with information pertinent to it
      layer.bindPopup("<h1>" + feature.properties.COUNTY_NAM + "</h1> <hr> <h2>" + feature.properties.COUNTY_NAM + "</h2>");

    }
  }).addTo(map);
});
