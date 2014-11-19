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
  console.log("Data for " + name);
  console.log(name_data[name]);
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

// Make a Venn diagram of dog colours
// Will only really work up to 4 colours that overlap
function makeVenn() {
  d3.text("data/color.csv", function(text) {
    var baseItems = {};
    var dataset = d3.csv.parseRows(text);

    // First build a set of the "base items", in this case the colours
    // We split on the "/" because sometimes there are combos of multiple colours,
    // for example "Black/Brown"; we want to record these as "black" and "brown"
    $.each(dataset, function(itemIndex, item) {
      var keys = item[0].split("/");
      var value = parseInt(item[1]);
      $.each(keys, function(keyIndex, key) {
        baseItems[key] === undefined ? baseItems[key] = value : baseItems[key] += value;
      });
    });
    var sets = [];

    // The indices dictionary maps the _name_ of the base item (e.g. "black")
    // to its index in the baseItems set; we can't predict ahead of time what
    // order those keys will be in
    var indices = {};
    $.each(Object.keys(baseItems), function(baseItemKeyIndex, baseItemKey) {
      sets.push({ label: baseItemKey, size: baseItems[baseItemKey] });
      indices[baseItemKey] = baseItemKeyIndex;
    });
    
    var results = [];
    
    // Need to get *all* possible combinations of base items (colours); code adapted from
    // http://www.growingwiththeweb.com/2013/06/algorithm-all-combinations-of-set.html
    for (var i = 0; i < sets.length; i++) {
      var resultsLength = results.length;
      for (var j = 0; j < resultsLength; j++) {
        var temp = results[j].slice(); // .slice() creates a deep copy of the array
        temp.push(indices[sets[i]["label"]]);
        results.push(temp);
      }
      results.push([indices[sets[i]["label"]]]);
    }

    // This will be used to build the overlaps array; even if a particular base item
    // combo has no matches, we need to initialize it to zero
    var interimResults = {};
    $.each(results, function(setIndex, set) {
      interimResults[set] = 0;
    });

    // Fill overlaps data
    $.each(dataset, function(itemIndex, item) {
      var keys = item[0].split("/");
      $.each(keys, function(keyIndex, key) {
        keys[keyIndex] = indices[key];
      })

      keys.sort();

      // Exclude sets that have only one item in them
      if (keys.length > 1) {
        var value = parseInt(item[1]);
        interimResults[keys] = value;
      }
    });

    // Finally, we can build the overlaps array
    var overlaps = [];
    $.each(Object.keys(interimResults), function(interimResultKeyIndex, interimResultKey) {
      if (interimResultKey.length > 1) {
        overlaps.push({ sets: interimResultKey.split(","), size: interimResults[interimResultKey]});
      }
    });

    // This is what's used by venn.js
    sets = venn.venn(sets, overlaps);

    var colorVenn = venn.drawD3Diagram(d3.select("#color_venn"), sets, 700, 700);

    var fillColors =   ["#000", "#abc", "#fff", "#643", "#999", "#f30"];
    var opacities =    [0.5,    0.5,    0.5,    0.5,    0.5,    0.5   ];
    var borderColors = ["#000", "#abc", "#ccc", "#421", "#999", "#f30"];
    var textColors =   ["#000", "#789", "#666", "#643", "#333", "#f30"];
    colorVenn.circles.style("fill", function(d, i) { return fillColors[i] })
                     .style("fill-opacity", function(d, i) { return opacities[i] })
                     .style("stroke", function(d, i) { return borderColors[i] })
                     .style("stroke-width", 1)
                     .style("stroke-opacity", 1)
    ;
    colorVenn.text.style("fill", function(d, i) { return textColors[i] })

  });
}

// Make a line diagram of lost dog counts
function makeLostAnimalsLineGraph() {
  
  var tooltip = d3.tip().attr('class', 'd3-tip').html(function(d) { return d["date_created"] + "<br/>" + parseInt(d["is_dog"]) + " dogs lost"; });

  var height = 500;
  var width = 1000;
  var margin = {top: 20, right:20, bottom: 50, left: 20};
  
  // formatters for axis and labels
  var decimalFormat = d3.format("0.2f");
  
  var svg = d3.select("#lost_dogs_graph")
    .append("svg")
    .attr("width", width + margin.right + margin.left)
    .attr("height", height + margin.top + margin.bottom)
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  
  svg.call(tooltip);

  svg.append("g")
    .attr("class", "y axis");
    
  svg.append("g")
    .attr("class", "x axis");
    
  var xScale = d3.scale.ordinal()
    .rangeRoundBands([margin.left, width], 0);
    
  var yScale = d3.scale.linear()
    .range([height, 10]);
  
  var xAxis = d3.svg.axis()
    .scale(xScale)
    .orient("bottom");
    
  var yAxis = d3.svg.axis()
    .scale(yScale)
    .orient("left");
  
  d3.csv("data/lost_by_date.csv", function(data) {
    
    // extract the x labels for the axis and scale domain
    var xLabels = data.map(function (d) { return d['date_created']; })
  
    xScale.domain(xLabels);
    yScale.domain([0, Math.round(d3.max(data, function(d) { return parseFloat(d['is_dog']); }))]);
    
    var line = d3.svg.line()
      .x(function(d) { return xScale(d['date_created']); })
      .y(function(d) { return yScale(d['is_dog']); });
    
    svg.append("path")
      .datum(data)
      .attr("class","line")
      .attr("d", line)

    
    svg.select(".x.axis")
      .attr("transform", "translate(0," + (height) + ")")
      .call(xAxis.tickValues(xLabels.filter(function(d, i) { 
        if (i % 3 == 0)
          return d;
        })))
      .selectAll("text")
      .style("text-anchor","end")
      .attr("transform", function(d) {
        return "rotate(-45)";
      });
    
    svg.select(".y.axis")
      .attr("transform", "translate(" + (margin.left) + ",0)")
      .call(yAxis);
    
    // x axis label
    svg.append("text")
      .attr("x", (width + (margin.left + margin.right) )/ 2)
      .attr("y", height + margin.bottom)
      .attr("class", "text-label")
      .attr("text-anchor", "middle")
      .text("Year-Month");
    
    var points = svg.selectAll(".point")
      .data(data)
      .enter().append("svg:circle")
       .attr("fill", function(d, i) { return "black" })
       .attr("cx", function(d, i) { return xScale(d['date_created']) })
       .attr("cy", function(d, i) { return yScale(d['is_dog']) })
       .attr("r", function(d, i) { return 4 })
       .on('mouseover', tooltip.show)
       .on('mouseout', tooltip.hide)

  });
}

loadNameData();

var types = ["name"];

// Make charts, Venn, line graphs
for (var i = 0; i < types.length; i++) { makeChart(types[i]) }
//makeVenn();
//makeLostAnimalsLineGraph();