// Functions for building map and pulling data for charts

function buildMap(month,year) {
  // Put the actual geojson here
  var geo_json = 'data/geo_json'
  var year_json = `data/inventory/${month}/${year}`
  console.log(year_json)
  
  // Use d3 to read in the geo_json file
  d3.json(geo_json).then(function(geo_data) {
    var geo_feat = geo_data.features;

    // read in states info
    var response = d3.json(year_json).then(function(response) {
      console.log(response);

      var counter = 0;
      for (var i=0; i<geo_feat.length; i++) {
        console.log(response.i);
        geo_feat[i].properties.RegionName = response[i].RegionName;
        geo_feat[i].properties.Number_of_Listings = response[i].Number_of_Listings;
        geo_feat[i].properties.Median_sqft_Value = response[i].Median_sqft_Value;
      };
    });
    

    // log to examine the data
    console.log(geo_data.features);
  
    // // fuction to be called on the data
    // createMap(data.features);
  });
};

buildMap('02',2019);

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