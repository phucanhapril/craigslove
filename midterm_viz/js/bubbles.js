
var draw = function(filepath) {

	var width = 2400,
		height = 3000,
		format = d3.format(",d"),
		color = d3.scale.category20c();

	var svg = d3.select("body").append("svg")
		.attr("width", width)
		.attr("height", height)
		.append("g")
		.attr("transform", "translate(200, 100)");

	d3.json(filepath, function(error, json) {
		if (error) throw error;
		var data = json.filter(function(d) {
			return d.frequencies[0].count >= 100;
		});
		var categories = data.map(function(d) { return d.name });

		for (var type in data) {
			var thisData = data[type].frequencies;
			var typeName = data[type].name;

			var domain = [ d3.min(thisData, function(d) { return d.count; }),
				d3.max(thisData, function(d) { return d.count }) ];
			var range = [50, 100];

			var radius = d3.scale.linear()
                    .domain(domain)
                    .range(range);

            var xLocation = d3.scale.linear()
            	.domain(range)
            	.range([0, width-400]);// TODO

            var wtf = d3.scale.linear()
            	.domain([0,10])
            	.range(domain);
			// add svg group for this category
			var group = svg.append("g")
				.attr("class", "row")
				.attr("transform", function(d, i) {
					var dy = type*200 + type*20;
					return "translate(0, " + dy + ")";
				});

			group.append("text")
				.attr("dx", "-180")
				.text(function(d) {
					return typeName;
				});

            var curr = 0;
			var node = group.selectAll(".node")
				.data(thisData)
				.enter().append("g")
				.attr("class", "node")
				.attr("transform", function(d, i) {
					return "translate("+xLocation(radius(wtf(i))) + ",0)";
				});



			node.append("circle")
				.attr("r", function(d) {
					return radius(d.count);//d.r;
				})

				.style("fill", function(d) {
					return color(type);
				});

			node.append("text")
				.attr("dy", ".3em")
				.style("text-anchor", "middle")
				.text(function(d) {
					return d.word;//d.className.substring(0, d.r / 3);
				});
			node.append("text")
				.attr("dy", "1.8em")
				.attr("class", "numLabel")
				.style("text-anchor", "middle")
				.attr("opacity", 0)
				.text(function(d) {
					return format(d.count);
				});

			node.on("mouseover", function() {
					d3.select(this).select('.numLabel').attr('opacity', 1);
				})
				.on("mouseout", function() {
					d3.select(this).select('.numLabel').attr('opacity', 0);
				});
		}
	});

};

$(document).ready(function() {
	console.log('ready');
	draw('../data/frequencies.json')
});