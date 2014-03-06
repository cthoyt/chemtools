function factorial(n) {
	if (n < 2) {
		return 1;
	}
	return n * factorial(n - 1);
}

function combinations(n, k) {
	return factorial(n) / (factorial(n - k) * factorial(k));
}

function makeSvgLineString(x1, y1, x2, y2, xScale, yScale, dotted) {
	var a = x1 * xScale;
	var b = y1 * yScale;
	var c = x2 * xScale;
	var d = y2 * yScale;
	if (dotted) {
		return '\t<line x1="' + a + '" y1="' + b + '" x2="' + c + '" y2="' + d + '" stroke="gray" stroke-width="1"/> \n';
	} else {
		return '\t<line x1="' + a + '" y1="' + b + '" x2="' + c + '" y2="' + d + '" stroke="black" stroke-width="1"/> \n';
	}
}

function makeTree(l) {

	var tree = [ [ [ 0, 0, 1 ] ] ];
	for (var level = 0; level < l.length; level++) {
		tree.push([]);
		var h = l[level][0];
		var j = l[level][1];
		for (var i = 0; i < tree[level].length; i++) {
			var start = tree[level][i][0] - h * j / 2.0;
			for (var k = 0; k <= h; k++)
				tree[level + 1].push([ start + k * j, i, tree[level][i][2] * combinations(h, k) ]);
		}
	}

	var frac_split = .6

	var xOffset = 0;
	for (var pos = 0; pos < tree[tree.length - 1].length; pos++)
		xOffset = Math.max(xOffset, tree[tree.length - 1][pos][0])

	xOffset += 2
		
	// # key = (point,point), value = labels
	tree[0][0] = [ [ xOffset, 0 ], 0, 1 ]

	var xScale = 25
	var yScale = 150

	var svg = makeSvgLineString(xOffset, 0, xOffset, frac_split, xScale, yScale, false)

	for (var level = 1; level < tree.length; level++) {
		for (var i = 0; i < tree[level].length; i++) {

			var currentXY = [ xOffset + tree[level][i][0], level ]
			var currentXDropY = [ currentXY[0], currentXY[1] + frac_split ]

			var parent_index = tree[level][i][1]
			var parentXY = tree[level - 1][parent_index][0]
			var parentXDropY = [ parentXY[0], parentXY[1] + frac_split ]

			svg += makeSvgLineString(currentXY[0], currentXY[1], parentXDropY[0], parentXDropY[1], xScale, yScale, true)

			if (tree.length - 1 != level) {
				svg += makeSvgLineString(currentXY[0], currentXY[1], currentXDropY[0], currentXDropY[1], xScale, yScale, false)
			} else {
				svg += makeSvgLineString(currentXY[0], currentXY[1], currentXY[0], currentXY[1] + .2, xScale, yScale, false)
			}
			tree[level][i] = [ currentXY, parent_index, tree[level][i][2] ]
		}
	}

	var highestY = tree.length + 1

	var maxRel = 0
	for (var index = 0; index < tree[tree.length - 1].length; index++)
		maxRel = Math.max(maxRel, tree[tree.length - 1][index][2])

	for (var el = 0; el < tree[tree.length - 1].length; el++) {
		var element = tree[tree.length - 1][el]
		x = element[0][0]
		h = 1.7 * element[2] / maxRel
		svg += makeSvgLineString(x, highestY, x, highestY - h, xScale, yScale, false)
	}

	svg += '<text x="15" y="' + highestY * yScale + 25 + '" fill="black">Splitting pattern of: ' + l + '</text>'

	return '<svg xmlns="http://www.w3.org/2000/svg">\n' + svg + "</svg>"
}

function makeBody() {

	var newLine = "%0D%0A"
	var path = location.href.split("?")
	var input = []
	if (path.length == 2) {
		var params = path[1].split("=")
		var unprocessed = params[1].split("%3B")

		for (var index = 0; index < unprocessed.length; index++) {
			input.push(unprocessed[index].split("%2C"))
		}

	}
	changeView(makeTree(input))
}

function changeView(str) {
	document.getElementById("place").innerHTML = str
}
