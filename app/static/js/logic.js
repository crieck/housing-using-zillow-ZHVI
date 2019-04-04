// init variables
  // Added code here
    // changed file to link to work with flask API
var geojson_data = 'data/geo_json';

const TWIN_CITIES_COORDINATES = [44.9833, -93.2667];

// init map object
var map = L.map("map", {
  center: TWIN_CITIES_COORDINATES,
  zoom: 11
});

// init tile layer
L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.light",
  accessToken: MAPBOX_API_KEY
}).addTo(map);

// Function that will determine the color of a Name based on the CTU_Type it belongs to
function chooseColor(CTU_Type) {
  switch (CTU_Type) {
  case "TOWNSHIP":
    return "brown";
  case "CITY":
    return "green";
  case "UNORGANIZED":
    return "black";
  default:
    return "black";
  }
}

// Grabbing our GeoJSON data..
d3.json(geojson_data, function(data) {
  // // Reset layers dictionary to be empty
    // Added code here
  layers = {};

  // Creating a geoJSON layer with the retrieved data
  L.geoJson(data, {
    // Style each feature (in this case a Name)
    style: function(feature) {
      return {
        color: "white",
        // Call the chooseColor function to decide which color to color our Name (color based on CTU_Type)
        fillColor: chooseColor(feature.properties.CTU_Type),
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
        // When a feature (Name) is clicked, it is enlarged to fit the screen
        click: function(event) {
          map.fitBounds(event.target.getBounds());
        }
      });
        // store reference
          // Added code here
        layers[feature.properties.Name] = layer;
        // Popup with region name, number of listings and median sqft
        layer.bindPopup("<h3>" + feature.properties.Name + "</h3> <hr> \
        <h4>Number of listings: " + feature.properties.Number_of_Listings + "</h4> <hr> \
        <h4>Median $ per square foot: " + feature.properties.Median_sqft_Value + '</h4>');

    }
  });
  
  // Added code here, not sure if layer would add to map if just defined as variable
  geo_layer.addTo(map);

});

// Added code here down
// Dictionary to store layer ids for updating popup content
  // Added reference to layer stored outside map
var layers = {};

// Fuction to tie sqlite data to features in map
  // Added function to tie in API data
function updatePopup(year_json) {
  // read in states info
  d3.json(year_json, function(response) {
      console.log(response);
      
      // loop through region json
      for (var i=0; i<response.length; i++) {
          // save regionName variable
          var region = response[i]['RegionName'];

          var layer = layers[region];

          // Giving each feature a pop-up with information pertinent to it
          layer.setPopupContent("<h3>" + region + "</h3> <hr> \
          <h4>Number of listings: " + response[i].Number_of_Listings + "</h4> <hr> \
          <h4>Median $/sqft: " + response[i].Median_sqft_Value + '</h4>');
      };
  });

};

// Set initial map to 2019
updatePopup(2019);

// Function to grab user input from html using d3/bootstrap slider
function inputYear(value) {
  // Flask link to zillow data API call
  var year_json = `data/inventory/02/${value}`;
  console.log(year_json);

  // change value/label of slider to new input
  document.getElementById("range").innerHTML = value;

  // change popup text to new year data
  updatePopup(year_json);
}

// Slider code
var initialYear = 2019;

// Select input on interaction and run input function
d3.select("#timeslide").on("input", function() {
  inputYear(this.value);
  console.log(this.value);
});

// Function that will change opacity if regions do not have housing data
function chooseOpacity(inventory) {
  switch (inventory) {
  case -1:
    return 0.5;
  default:
    return 0.75;
  }
}