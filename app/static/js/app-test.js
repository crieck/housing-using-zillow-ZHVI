// Fuction to tie sqlite data to features in map
function updatePopup(feature, layer) {
    // Flask link to zillow data API call
    var year_json = `data/inventory/02/${year}`
    // assuming here key is in feature.properties.name = 'Ward01'
    // read in states info
    d3.json(year_json).then(function(response) {
        console.log(response);
        
        // loop through region json
        for (var i=0; i<response.length; i++) {
            // save regionName variable
            var region = response[i]['RegionName'];

            // check if region is the same as the feature.name, update listings and price
            if (region = feature.properties.Name) {
                feature.properties.Number_of_Listings = response[i].Number_of_Listings;
                feature.properties.Median_sqft_Value = response[i].Median_sqft_Value;
                return;
            }
        };
    });

    // Giving each feature a pop-up with information pertinent to it
    layer.setPopupContent("<h1>" + feature.properties.Name + "</h1> <hr> <h2>" + feature.properties.CTU_Type + "</h2> <hr> \
    <h3>Number of listings: " + feature.properties.Number_of_Listings + "</h3> <hr> \
    <h3>Median $ per square foot: " + feature.properties.Median_sqft_Value + '</h3>');
}

// Function to grab user input from map
control.on('click', function(event) {
    var userinput = event.data/input/value
    return `data/inventory/02/${userinput}`
}

group.eachLayer(function (layer) {
    layer.bindPopup('Hello');
});


updateFeature(feature, marker) {
    // feature = updated js object of your feature data
    // marker = leaflet marker object
   
   return marker // important!
   }