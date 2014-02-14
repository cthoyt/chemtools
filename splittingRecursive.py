import functools
import itertools
import math
import string
import subprocess
import sys


def rangeList(start, stop, step):
	while start <= stop:
		yield start
		start += step

def combinations(n, k):
	return math.factorial(n) / (math.factorial(k) * math.factorial(n - k))

def splitter(l):
	l = sorted(l, key = lambda entry: entry[1])[::-1]

	# tree[level][index] === (coordinate, parent index, relative height)
	tree = [[(0, 0, 1)]]

	for level in xrange(len(l)):

		tree.append([])
		h = l[level][0]
		j = l[level][1]

		for i in xrange(len(tree[level])):
			# shift-width
			start = tree[level][i][0] - h * j / 2.0
			for k in xrange(h + 1):
				tree[level + 1].append((start + k * j, i, combinations(h, k)))
				
	return tree

def extractPatternFromTree(tree):
	for level in xrange(1, len(tree) - 1):
		for i in xrange(len(tree[level])):
			parent = tree[level][i][1]
			tree[level][i] = (tree[level][i][0], tree[level][i][1], tree[level][i][2] * tree[level - 1][parent][2])
	return {key:value for key, drop, value in tree[len(tree) - 1]}

def prepareResonanceTex(patternTree):
	pass

def prepareSplittingTex(tree):
	
	width = 0
	xOffset = width / 2
	yOffset = 0
	scaleX = 1  # (middle - 2 * horizontalPadding) / tree[len(tree) - 1][0][0]
	scaleY = 1
	frac_split = .75

	resonanceCommands = []	
"""
	bottom = yOffset - (len(tree) - 1 + frac_split) * scaleY
	pattern = extractPatternFromTree(tree)
	for x in pattern:
		resonanceCommands.append("\t\t\\draw " + str((x, bottom)) + " -- " + str((x, bottom + pattern[x])) + " ;")
"""	

	solidCommands = ["\t\t\\draw (0," + str(scaleY * frac_split) + ") -- (0,0) ;"]
	dottedCommands = []
	
	tree[0][0] = (xOffset, yOffset * frac_split)
	
	for level in xrange(1, len(tree)):
		for i in xrange(len(tree[level])):

			currentXY = (xOffset + tree[level][i][0] * scaleX, yOffset - level * scaleY)
			currentXDropY = (currentXY[0], currentXY[1] - frac_split * scaleY)

			parent_index = tree[level][i][1]
			parentXY = tree[level - 1][parent_index]

			# if last line (level = len(tree) - 1, draw longer tail  if level == len(tree): b = (a[0], a[1] + levelScaleY

			dottedCommands.append("\t\t\\draw [dotted] " + str(parentXY) + " -- " + str(currentXY) + " ;")
			solidCommands.append("\t\t\\draw " + str(currentXY) + " -- " + str(currentXDropY) + " ;")

			tree[level][i] = currentXDropY

	return string.join(solidCommands, "\n") + "\n\n" + string.join(dottedCommands, "\n") + "\n\n" + string.join(resonanceCommands, "\n") + "\n"

def prepareTexHeader(width = 0.3, height = 150):
	return "\\documentclass[]{article}\n\n\\usepackage{tikz}\n\\usepackage[margin=1in]{geometry}\n\n\\begin{document}\n\n\\begin{figure}\n\t\\centering\n\t\\begin{tikzpicture}[x=" + str(width) + "cm, y=" + str(height) + "]\n"


def prepareTexFooter(caption = "splitting tree"):
    return "\t\\end{tikzpicture}\n\t\\caption{" + str(caption) + "}\n\\end{figure}\n\n\\end{document}"

def getTex(l):
	tree = splitter(l)
	return prepareTexHeader() + prepareSplittingTex(tree) + prepareTexFooter(l)

def strToFile(str, fname):
	f = open(fname, 'w')
	f.write(str)
	f.close()

def getSplitsFromUser():
	return [(input("hydrogens on split #" + str(i + 1) + "? "), input("coupling constant for split #" + str(i + 1) + "? ")) for i in xrange(input("number of splits? "))]

def readSplitsFromFile(fname):
	with open(fname) as f:
		return [(int(h), float(j)) for h, j in [string.split(line.strip(), ",") for line in f]]


def testProcess():
	test1 = ([(1, 5)], {-2.5: 1, 2.5: 1})
	test2 = ([(1, 4)], {-2: 1, 2: 1})
	test3 = ([(2, 4)], {-4: 1, 0: 2, 4: 1})
	test4 = ([(2, 5)], {-5: 1, 0: 2, 5: 1})
	test5 = ([(3, 4)], {-6: 1, -2: 3, 2: 3, 6: 1})
	test6 = ([(3, 5)], {-7.5: 1, -2.5: 3, 2.5: 3, 7.5: 1})
	test7 = ([(1, 6), (1, 2)], {-4: 1, -2: 1, 2: 1, 4: 1})
	test8 = ([(1, 8), (1, 4), (1, 2)], {key: 1 for key in rangeList(-7.0, 7.0, 2.0)})
	data = [test1, test2, test3, test4, test5, test6, test7, test8]
	for test, result in data:
 		assert extractPatternFromTree(splitter(test)) == result

testProcess()



# ## BEGIN SCRIPT

if len(sys.argv) == 3:
	l = readSplitsFromFile(sys.argv[1])
	strToFile(getTex(l), sys.argv[2])
	if subprocess.call(["which", "pdflatex"]) == 0:
		subprocess.call(["pdflatex", sys.argv[2]])
	else:
		print "Missing pdflatex!\nNo pdf produced!\nRaw LaTeX output at:", sys.argv[2]

else:
	l = getSplitsFromUser()
	strToFile(getTex(l), input("output file name? "))
