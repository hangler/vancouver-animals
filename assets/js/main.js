// Load the name data
var name_data = {};
function loadNameData() {
  // First, load the data
  d3.text("data/name_stats.csv", function(text) {
    var dataset = d3.csv.parseRows(text);
    var columns;
    $.each(dataset, function(rowIndex, row) {
      if (rowIndex == 0) {
        columns = row;
        return;
      }
      var node = buildNode(columns, row);
      name_data[node["name"]] = node;
    });

    // Now, build the chart
    makeChart("name");
  });
}

// Given a row from a CSV [1, 2, 3] and its columns [a, b, c],
// build an object such that obj[a] = 1, obj[b] = 2, etc.
function buildNode(columns, row) {
  var node = {};
  $.each(columns, function(itemIndex, item) {
    node[item] = row[itemIndex];
  });
  return node;
}

// Show name data
function showNameData(name) {
  var node = name_data[name];
  $(".data_content.name").text(node["name"]);
  $(".data_content.m").text(parseInt(node["m"]));
  $(".data_content.f").text(parseInt(node["f"]));
}

// Generic method to make a bar chart
function makeChart(type) {
  d3.text("data/" + type + ".csv", function(text) {
    var dataset = d3.csv.parseRows(text);
    var maxLength = dataset[0][1]
    d3.select("#" + type + "_chart")
        .selectAll("div")
        .data(dataset)
        .enter()
          .append("div")
          .style("width", function(d) { return (d[1] / maxLength) * 100 + "%"; })
          .text(function(d) { return d[0] + " (" + d[1] + ")"; })
          .on("click", function(d) { showNameData(d[0]) });
    
  }); 
}

loadNameData();