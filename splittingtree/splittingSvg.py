
import sys
import numpy
from operator import itemgetter
import argparse

def getSplitsFromUser():
	h = int(input("number of types of magnetically eq. hydrogens? "))
	return [(input("hydrogens on split #" + str(i + 1) + "? "),
			 input("coupling constant for split #" + str(i + 1) + "? ")) for i in range(h)]


def readSplitsFromFile(fname):
	with open(fname) as f:
		fi = (line.strip().split(",") for line in f)
		return [(int(h), float(j)) for h, j in fi]


def strToFile(str, fname):
	with open(fname, 'w') as out:
		out.write(str)


def makeSvgLineString(p1, p2, xScale, yScale, dotted = False):
	points = (xScale * p1[0], yScale * p1[1], xScale * p2[0] , yScale * p2[1])
	color = 'gray' if dotted else 'black'
	if dotted:
		return '\t<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="gray" stroke-width="1"/> \n' % points
	else:
		return '\t<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="black" stroke-width="1"/> \n' % points


def makeSVG(l):
	l = sorted(l, key=itemgetter(1), reversed=True)

	# tree[level][index] === (coordinate, parent index, relative height)
	tree = [[(0, 0, 1)]]

	# load up the tree
	for level in range(len(l)):
		tree.append([])
		h = l[level][0]
		j = l[level][1]
		for i in range(len(tree[level])):
			start = tree[level][i][0] - h * j / 2.0
			for k in range(h + 1):
				combinations = numpy.misc.combinations(h, k)
				tree[level + 1].append((start + k * j, i, tree[level][i][2] * combinations))

	frac_split = .6

	xOffset = max([el[0] for el in tree[len(tree) - 1]])

	# key = (point,point), value = labels
	tree[0][0] = ((xOffset, 0), 0 , 1)

	xScale = 10
	yScale = 100

	svg = makeSvgLineString((xOffset, 0), (xOffset, frac_split), xScale, yScale)

	for level in range(1, len(tree)):
		for i in range(len(tree[level])):

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

	highestY = len(tree) + 1
	maxRel = max([el[2] for el in tree[len(tree) - 1]])

	for el in tree[len(tree) - 1]:
		x = el[0][0]
		h = 1.7 * el[2] / maxRel
		svg += makeSvgLineString((x, highestY), (x, highestY - h), xScale, yScale)

	svg += '<text x="15" y="' + str(highestY * yScale + 25) + '" fill="black">Splitting pattern of: ' + str(l) + '</text>'


	return '<?xml version="1.0"?>\n<svg xmlns="http://www.w3.org/2000/svg">\n' + svg + "</svg>"

l = []
fileName = ""

if len(sys.argv) == 3:
	l = readSplitsFromFile(sys.argv[1])
	fileName = sys.argv[2]
else:
	l = getSplitsFromUser()
	fileName = input("file name in quotes (no extension)? ") + ".svg"

output = makeSVG(l)
strToFile(output, fileName)


pa = argparse.ArgumentParser()
pa.add_argument("-s", dest='splits', nargs='2', metavar=('number_hydrogens', 'coupling_constant'), action='append')
pa.add_argument('-o', dest='output', default=sys.stdout, type=argparse.FileType('w'))
args = pa.parse_args()

