var NetworkModule = function(svg_width, svg_height) {

    // Create the svg tag:
    var svg_tag = "<svg  id='NetworkModule_d3' width='" + svg_width + "' height='" + svg_height + "' " +
        "style='border:1px dotted'></svg>";

    // Append svg to #elements:
    $("#elements")
        .append($(svg_tag)[0]);

    var svg = d3.select("#NetworkModule_d3")
    var width = +svg.attr("width")
    var height = +svg.attr("height")
    var g = svg.append("g")
            .classed("network_root", true)
            .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")")

    var tooltip = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);

    svg.call(d3.zoom()
        .on("zoom", function() {
            g.attr("transform", d3.event.transform);
        }));

    svg.append("svg:defs").selectAll("marker")
        .data(["end"])      // Different link/path types can be defined here
        .enter().append("svg:marker")    // This section adds in the arrows
        .attr("id", String)
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 15)
        .attr("refY", 0)
        .attr("markerWidth", 5)
        .attr("markerHeight", 10)
        .attr("orient", "auto")
        .append("svg:path")
        .attr("d", "M0,-2L10,0L0,2");

    var paths = g.append("g")
        .attr("class", "paths")
 
    var nodes = g.append("g")
        .attr("class", "nodes")

    this.render = function(data) {
        var graph = JSON.parse(JSON.stringify(data));

        simulation = d3.forceSimulation()
        .nodes(graph.nodes)
        .force("charge", d3.forceManyBody()
            .strength(-80)
            .distanceMin(2))
        .force("link", d3.forceLink(graph.edges))
        .force("center", d3.forceCenter())
        .stop();

        for (var i = 0, n = Math.ceil(Math.log(simulation.alphaMin()) / Math.log(1 - simulation.alphaDecay())); i < n; ++i) {
            simulation.tick();
        }

    paths
        .selectAll("line")
            .data(graph.edges)
            .enter()
            .append("path")
            .on("mouseover", function(d) {
                tooltip.transition()
                    .duration(200)
                    .style("opacity", .9);
                tooltip.html(d.tooltip)
                    .style("left", (d3.event.pageX) + "px")
                    .style("top", (d3.event.pageY) + "px");
            })
            .on("mouseout", function() {
                tooltip.transition()
                    .duration(500)
                    .style("opacity", 0);
            });
    
    paths
        .selectAll("path")
            .data(graph.edges)
            .attr("xmlns","http://www.w3.org/2000/svg")
            .attr("fill-opacity","0%")
            .attr("d", function(d) {
                raio = Math.abs(d.source.x - d.target.x)+Math.abs(d.source.y - d.target.y);
                return "M "+
                d.source.x+" "+d.source.y+" A "+raio+","+raio+" 0 0,1 "+d.target.x+" "+ d.target.y; 
            })
            .attr("stroke-width", function(d) { return d.width; })
            .attr("stroke", function(d) { return d.color; })
            .attr("marker-end", function(d) {
                return d.directed ? "url(#end)" : ""
            });
 
    paths
        .selectAll("path")
            .data(graph.edges)
            .exit()
            .remove();

    nodes
        .selectAll("circle")
            .data(graph.nodes)
            .enter()
            .append("circle")
            .on("mouseover", function(d) {
                tooltip.transition()
                    .duration(200)
                    .style("opacity", .9)
                    .style("font-family", "courier")
                    .style("font-size", "15px");
                tooltip.html(d.tooltip)
                    .style("font-size", "15px")
                    .style("font-family", "courier")
                    .style("left", (d3.event.pageX) + "px")
                    .style("top", (d3.event.pageY) + "px");
            })
            .on("mouseout", function() {
                tooltip.transition()
                    .duration(500)
                    .style("font-family", "courier")
                    .style("font-size", "15px")
                    .style("opacity", 0);
            });

    nodes
        .selectAll("circle")
            .data(graph.nodes)
            .attr("cx", function(d) {return d.x; })
            .attr("cy", function(d) { return d.y; })
            .attr("r", function(d) { return d.size; })
            .attr("fill", function(d) { return d.color; })

    nodes
        .selectAll("circle")
            .data(graph.nodes)
            .exit()
                .remove();
    };

    this.reset = function() {

    };
};
