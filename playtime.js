function factorial(n) {
	if (n < 2) {
		return 1;
	}
	return n * factorial(n - 1);
}

function combinations(n, k) {
	return factorial(n) / (factorial(n - k) * factorial(k));
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
	return tree;
}

function makeSvgLine(x1, y1, x2, y2, dotted) {
	if (dotted) {
		return '\t<line x1="' + x1 + '" y1="' + y1 + '" x2="' + x2 + '" y2="' + y2 + '" stroke="gray" stroke-width="1"/> \n';
	} else {
		return '\t<line x1="' + x1 + '" y1="' + y1 + '" x2="' + x2 + '" y2="' + y2 + '" stroke="black" stroke-width="1"/> \n';
	}
}

function nextPart() {
	var frac_split = .6

	xOffset = max([el[0] for el in Iterator(tree[tree.length - 1])])

	//# key = (point,point), value = labels
	tree[0][0] = ((xOffset, 0), 0 , 1)

	xScale = 10
	yScale = 100

	svg = makeSvgLineString((xOffset, 0), (xOffset, frac_split), xScale, yScale)

	for level in xrange(1, len(tree)):
		for i in xrange(len(tree[level])):

			currentXY = (xOffset + tree[level][i][0], level)
			currentXDropY = (currentXY[0], currentXY[1] + frac_split)

			parent_index = tree[level][i][1]
			parentXY = tree[level - 1][parent_index][0]
			parentXDropY = (parentXY[0], parentXY[1] + frac_split)

			svg += makeSvgLineString(currentXY, parentXDropY, xScale, yScale, True)

			if not len(tree) - 1 == level:
				svg += makeSvgLineString(currentXY, currentXDropY, xScale, yScale)
			else:
				svg += makeSvgLineString(currentXY, (currentXY[0], currentXY[1] + .2), xScale, yScale)

			tree[level][i] = (currentXY, parent_index, tree[level][i][2])
}

function makeBody() {

	var newLine = "%0D%0A"
	var path = location.href.split("?")
	if (path.length == 2) {
		var params = path[1].split("=")
		if (params.length == 2) {
			changeView(params[1]);
			changeView(params[1].split(newLine)[0].split("+")[0]);

			for ( var str in params[1].split(newLine)) {
				alert(str.split("+")[0])
			}
		}
	}
	var tree = makeTree([ [ 3, 6 ], [ 2, 7 ] ])
	changeView(tree[0]);
	alert()
	changeView(tree[1])
	alert()
	changeView(tree[2][0])
}

function changeView(str) {
	document.getElementById("place").innerHTML = str
}
