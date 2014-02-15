import functools
import itertools
import math
import string
import subprocess
import sys

# utilities
def rangeList(start, stop, step):
	while start <= stop:
		yield start
		start += step

def combinations(n, k):
	return math.factorial(n) / (math.factorial(k) * math.factorial(n - k))

def transformCoordinates(l, xScale, yScale, xOffset, yOffset):
	return [transformCoordinate((x, y), xScale, yScale, xOffset, yOffset) for x, y in l]

def transformCoordinate(p, xScale, yScale, xOffset, yOffset):
	return (xOffset + xScale * p[0], yOffset + yScale * p[1])

# i/o
def getSplitsFromUser():
	return [(input("hydrogens on split #" + str(i + 1) + "? "), input("coupling constant for split #" + str(i + 1) + "? ")) for i in xrange(input("number of splits? "))]

def readSplitsFromFile(fname):
	with open(fname) as f:
		return [(int(h), float(j)) for h, j in [string.split(line.strip(), ",") for line in f]]

def strToFile(str, fname):
	f = open(fname, 'w')
	f.write(str)
	f.close()

def makeSvgLineString(p1, p2, xScale, yScale, dotted = False):
	points = (xScale * p1[0], yScale * p1[1], xScale * p2[0] , yScale * p2[1])
	if dotted:
		return '\t<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="blue" stroke-width="2"/> \n' % points
	else:
		return '\t<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="black" stroke-width="2"/> \n' % points

def makeSVG(l):
	l = sorted(l, key = lambda entry: entry[1])[::-1]

	# tree[level][index] === (coordinate, parent index, relative height)
	tree = [[(0, 0, 1)]]

	# load up the tree
	for level in xrange(len(l)):
		tree.append([])
		h = l[level][0]
		j = l[level][1]
		for i in xrange(len(tree[level])):
			start = tree[level][i][0] - h * j / 2.0
			for k in xrange(h + 1):
				tree[level + 1].append((start + k * j, i, tree[level][i][2] * combinations(h, k)))

	frac_split = .6

	xOffset = max([el[0] for el in tree[len(tree) - 1]])

	# key = (point,point), value = labels
	tree[0][0] = (xOffset, 0)

	xScale = 10
	yScale = 100

	svg = makeSvgLineString((xOffset, 0), (xOffset, frac_split), xScale, yScale)

	for level in xrange(1, len(tree)):
		for i in xrange(len(tree[level])):

			currentXY = (xOffset + tree[level][i][0], level)
			currentXDropY = (currentXY[0], currentXY[1] + frac_split)

			parent_index = tree[level][i][1]
			parentXY = tree[level - 1][parent_index]
			parentXDropY = (parentXY[0], parentXY[1] + frac_split)

			svg += makeSvgLineString(currentXY, parentXDropY, xScale, yScale, True)
			svg += makeSvgLineString(currentXY, currentXDropY, xScale, yScale)

			tree[level][i] = currentXY

	# DRAW RESONSANCE HERE

	highestY = tree[len(tree) - 1][0][1]
	range = highestY - level - frac_split

	return '<?xml version="1.0"?>\n<svg xmlns="http://www.w3.org/2000/svg">\n' + svg + "</svg>"

# ## BEGIN SCRIPT
l = []
fileName = ""

if len(sys.argv) == 3:
	l = readSplitsFromFile(sys.argv[1])
	fileName = sys.argv[2]
else:
	l = getSplitsFromUser()
	fileName = input("file name? ")

output = makeSVG(l)
strToFile(output, fileName + ".txt")
strToFile(output, fileName + ".svg")

