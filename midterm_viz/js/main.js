var draw = function(filepath) {

	var margin = {
			top: 20,
			right: 20,
			bottom: 100,
			left: 60
		},
		width = 1600 - margin.left - margin.right,
		height = 800 - margin.top - margin.bottom;

	var x0 = d3.scale.ordinal()
		.rangeRoundBands([0, width], .1);

	var x1 = d3.scale.ordinal();

	var y = d3.scale.linear()
		.range([height, 0]);

	var color = d3.scale.ordinal()
		.range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);

	var xAxis = d3.svg.axis()
		.scale(x0)
		.orient("bottom");

	var yAxis = d3.svg.axis()
		.scale(y)
		.orient("left")
		.tickFormat(d3.format(".2s"));

	var svg = d3.select("body").append("svg")
		.attr("width", width + margin.left + margin.right)
		.attr("height", height + margin.top + margin.bottom)
		.append("g")
		.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	d3.json(filepath, function(error, json) {
		if (error) throw error;
		var data = json.sort(function(a, b) {
			return b.values[0].value - a.values[0].value;
		});
		var words = data.map(function(d) {
			return d.word;
		});

		var categories = data[0]['values'].map(function(d) {
			return d.category;
		});

		x0.domain(words);
		x1.domain(categories).rangeRoundBands([0, x0.rangeBand()]);
		y.domain([0, d3.max(data, function(d) {
			return d3.max(d.values, function(d) {
				return d.value;
			});
		})]);

		svg.append("g")
			.attr("class", "x axis")
			.attr("transform", "translate(0," + height + ")")
			.call(xAxis)
			.selectAll("text")
		    .attr("y", 0)
		    .attr("x", 9)
		    .attr("dy", "1em")
		    .attr("transform", "rotate(45)")
		    .style("text-anchor", "start");

		svg.append("g")
			.attr("class", "y axis")
			.call(yAxis)
			.append("text")
			.attr("transform", "rotate(-90)")
			.attr("y", 6)
			.attr("dy", ".71em")
			.style("text-anchor", "end")
			.text("word frequency");

		var word = svg.selectAll(".word")
			.data(data)
			.enter().append("g")
			.attr("class", "word")
			.attr("transform", function(d) {
				return "translate(" + x0(d.word) + ",0)";
			});

		word.selectAll("rect")
			.data(function(d) {
				return d.values;
			})
			.enter().append("rect")
			.attr("width", x1.rangeBand())
			.attr("x", function(d) {
				return x1(d.category);
			})
			.attr("y", function(d) {
				return y(d.value);
			})
			.attr("height", function(d) {
				return height - y(d.value);
			})
			.style("fill", function(d) {
				return color(d.category);
			})
			.on("mouseover", function(d) {
					console.log(d.category + ", " + d.value);
				})
				.on("mouseout", function() {
					//d3.select(this).select('.numLabel').attr('opacity', 0);
				});
	});

};


$(document).ready(function() {
	console.log('ready');
	draw('../data/frequencies_relative.json')
});