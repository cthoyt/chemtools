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
	l = sorted(l, key = lambda entry: entry[1])

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
		# sort?
		# sorted(tree[level + 1], key = lambda el: el[0])
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
    #in relative units
	height = 1100
	width = 850
	verticalPadding = 5
	horizontalPadding = 5
    
    
    	#todo: calculate these based on height/width/padding 
	scaleX = 1
	levelScaleY = 1
	frac_split = .7
    
	dottedLineCommands = []
	solidLineCommands = []
	drawPointCommands = []
    
	coordinateNumber = 1
	for level in xrange(1, len(tree) - 1):
		for i in xrange(len(tree[level])):
            
		parent_index = tree[level][i][1]
		relativeX = tree[level][i][0]
		cartesianCoordinate = (relativeX * scaleX, level * levelScaleY)
            
			tree[level][i] = (coordinateNumber, parent_index, cartesianCoordinate)
			
			#todo:
			#draw and label current point
			#draw solid line from (x,y) = tree[level - 1][parent_index][0] to (x, y + frac_split * levelScaleY)
			#if last line (level = len(tree) - 1, draw longer tail
			
			#draw dotted line from (x, y + frac_split * levelScaleY) if (x,y) = tree[level - 1][parent_index][0] i.e. coordinate number to current coordinate number
			
			coordinateNumber += 1
			
			
	points = string.join(drawPointCommands, "\n")
	solids = string.join(solidLineCommands, "\n")
	dotted = string.join(solidLineCommands, "\n")
	
	return points + "\n\n" + solids + "\n\n" + dotted

def prepareTexHeader():
    pass

def prepareTexFooter():
    pass

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

tree = splitter([(1, 8), (1, 4), (1, 2)])
print(tree)
print(extractPatternFromTree(tree))
