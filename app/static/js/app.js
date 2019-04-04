
// Functions for updating data in geojson
function updateData(month,year) {
  // Flask links to data pulls from geo_json and sqlite database
  var geo_json = 'data/geo_json'
  var year_json = `data/inventory/${month}/${year}`
  console.log(year_json)
  
  // Use d3 to read in the geo_json file
  d3.json(geo_json).then(function(geo_data) {
    var geo_feat = geo_data.features;

    // read in states info
    var response = d3.json(year_json).then(function(response) {
      console.log(response);

      // loop through region json
      for (var i=0; i<response.length; i++) {
        // save regionName variable
        var region = response[i]['RegionName'];

        // loop through geo_json
        for (var j=0; j<geo_feat.length; j++) { 
          // check if regionName matches the geo_json data, update listings and price
          while (geo_feat[j].properties.Name === region) {
            geo_feat[j].properties.Number_of_Listings = response[i].Number_of_Listings;
            geo_feat[j].properties.Median_sqft_Value = response[i].Median_sqft_Value;
            return;
          };
        };
      };
    });

    // log to examine the data
    console.log(geo_data.features);
  
    // // fuction to be called on the data
    // createMap(data.features);
  });
};

updateData('02',2019);

// function buildCharts(sample) {
//   // url for samples data
//   var sample_url = `samples/${sample}`;
//   console.log(sample_url);

//   // Use `d3.json` to fetch the sample data for the plots
//   d3.json(sample_url).then(function(response) {
//     console.log(response);

// function init() {
//   // Grab a reference to the dropdown select element
//   var selector = d3.select("#selDataset");

//   // Use the list of region names to populate the select options
//   d3.json("/regions").then((regionNames) => {
//     regionNames.forEach((region) => {
//       selector
//         .append("option")
//         .text(region)
//         .property("value", region);
//     });

//     // Use the first sample from the list to build the initial plots
//     // Mpls should be first region
//     const firstRegion = regionNames[0];
//     buildCharts(firstRegion);
//     buildMap(02,2019);
//   });
// };

// function optionChanged(newRegion) {
//   // Fetch new data and build a chart each time a new region is selected
//   buildCharts(newRegion);
// };