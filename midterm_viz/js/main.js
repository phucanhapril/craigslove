
var draw = function(filepath) {

	var diameter = 960,
		format = d3.format(",d"),
		color = d3.scale.category20c();

	var bubble = d3.layout.pack()
		.sort(null)
		.size([diameter, diameter])
		.padding(1.5);

	var svg = d3.select("body").append("svg")
		.attr("width", diameter)
		.attr("height", diameter)
		.attr("class", "bubble");

	d3.json(filepath, function(error, json) {
		if (error) throw error;
		var data = formatData(json);
		console.log(data);
		var node = svg.selectAll(".node")
			.data(bubble.nodes(classes(data))
				.filter(function(d) {
					return !d.children;
				}))
			.enter().append("g")
			.attr("class", "node")
			.attr("transform", function(d) {
				return "translate(" + d.x + "," + d.y + ")";
			});

		// node.append("title")
		// 	.text(function(d) {
		// 		return d.className + ": " + format(d.value);
		// 	});

		node.append("circle")
			.attr("r", function(d) {
				return d.r;
			})
			.style("fill", function(d) {
				return color(d.packageName);
			});

		node.append("text")
			.attr("dy", ".3em")
			.style("text-anchor", "middle")
			.text(function(d) {
				return d.className.substring(0, d.r / 3);
			});
		node.append("text")
			.attr("dy", "1.8em")
			.attr("class", "numLabel")
			.style("text-anchor", "middle")
			.attr("opacity", 0)
			.text(function(d) {
				return format(d.value);
			});

		node.on("mouseover", function() {
				d3.select(this).select('.numLabel').attr('opacity', 1);
			})
			.on("mouseout", function() {
				d3.select(this).select('.numLabel').attr('opacity', 0);
			});
	});

};

// Returns a flattened hierarchy containing all leaf nodes under the root.
var classes = function(root) {
  var classes = [];

  function recurse(name, node) {
    if (node.children) node.children.forEach(function(child) { recurse(node.name, child); });
    else classes.push({packageName: name, className: node.name, value: node.size});
  }

  recurse(null, root);
  return {children: classes};
}

var formatData = function(json) {
	var root = {
		name: 'root',
		children: [],
		size: 0
	};
	for (var i = 0; i < json.length; i++) {
		var o = {
			name: json[i].name,
			size: 0,
			children: []
		};
		var oSize = 0;
		var frequencyList = json[i].frequencies;
		for (var j = 0; j < frequencyList.length; j++) {
			var o2 = {
				name: frequencyList[j].word,
				size: frequencyList[j].count,
				children: null
			};
			o.children.push(o2)
			o.size += frequencyList[j].count;
			root.size += frequencyList[j].count;
			
		}
		if (o.size > 400) {
			root.children.push(o);
		}
		
	}
	return root;
};
$(document).ready(function() {
	console.log('ready');
	draw('../data/frequencies.json')
});