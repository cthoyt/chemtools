import itertools
import string
from subprocess import call
import sys


def makeSplittingList(l):
    # input list of doubles as (number hydrogens, coupling constant in hz)
    # output list of doubles as (relative coordinate, peak height)
    # produces a first-order coupling tree centered at zero with ratios of heights

	# count the number of each type of splitting
	splits = []
	for num_hydrogen, j in l:
		splits.extend(j for i in rangeList(1, num_hydrogen, 1))

	# challenge: recursive implementation (because why not)
	# populate a list of the locations of each split
	shifts = reduce(lambda shifts, j: itertools.chain(*[rangeList(shift - j / 2.0, shift + j / 2.0, j) for shift in shifts]), splits, [0])

	# count the frequency at each point as relative heights
	answer = {}
	for s in shifts:
			answer[s] = 1 if s not in answer else answer[s] + 1

	return answer

def test_makeSplittingList():
	test1 = ([(1, 5)], {-2.5: 1, 2.5: 1})
	test2 = ([(1, 4)], {-2: 1, 2: 1})
	test3 = ([(2, 4)], {-4: 1, 0: 2, 4: 1})
	test4 = ([(2, 5)], {-5: 1, 0: 2, 5: 1})
	test5 = ([(3, 4)], {-6: 1, -2: 3, 2: 3, 6: 1})
	test6 = ([(3, 5)], {-7.5: 1, -2.5: 3, 2.5: 3, 7.5: 1})
	test7 = ([(1, 4), (1, 2)], {-3: 1, -1: 1, 1: 1, 3: 1})
	test8 = ([(1, 8), (1, 4), (1, 2)], {key: 1 for key in rangeList(-7.0, 7.0, 2.0)})
	data = [test1, test2, test3, test4, test5, test6, test7, test8]
	for test, result in data:
		assert makeSplittingList(test) == result

def rangeList(start, stop, step):
	while start <= stop:
		yield start
		start += step

def test_rangeList():
	test1 = (0, 3, 1, [0, 1, 2, 3])
	test2 = (-2.5, 2.5, 5, [-2.5, 2.5])
	test3 = (-7.5, 7.5, 5, [-7.5, -2.5, 2.5, 7.5])
	data = [test1, test2, test3]
	for start, stop, step, result in data:
		assert list(rangeList(start, stop, step)) == result

def prepTex(l, caption):
	# input a splitting dictionary
	# output TeX string

	width = 0.3
	texStr = "\\documentclass[]{article}\n\n\\usepackage{tikz}\n\\usepackage[margin=1in]{geometry}\n\n\\begin{document}\n\n\\begin{figure}\n\t\\centering\n\t\\begin{tikzpicture}[x=" + str(width) + "cm]\n"

	for shift, height in l.iteritems():
		texStr += "\t\t\\draw (" + str(shift) + "," + str(height) + ") -- (" + str(shift) + ", 0) ;\n"

	texStr += "\t\\end{tikzpicture}\n\t\\caption{" + caption + "}\n\\end{figure}\n\n\\end{document}"
	return texStr

def strToFile(str, fname):
	f = open(fname, 'w')
	f.write(str)
	f.close()

def getSplitsFromUser():
	return [(input("hydrogens on split #" + str(i + 1) + "? "), input("coupling constant for split #" + str(i + 1) + "? ")) for i in xrange(input("number of splits? "))]

def readSplitsFromFile(fname):
	with open(fname) as f:
		return [(int(h), float(j)) for h, j in [string.split(line.strip(), ",") for line in f]]

# ## BEGIN SCRIPT

test_rangeList()
test_makeSplittingList()

if len(sys.argv) == 3:
	n = readSplitsFromFile(sys.argv[1])
	strToFile(prepTex(makeSplittingList(n), str(n)), sys.argv[2])
#	if call(["which", "pdflatex"]):
	call(["pdflatex", sys.argv[2]])
#	else:
#		print("TeX missing!")
else:
	n = getSplitsFromUser()
	strToFile(prepTex(makeSplittingList(n), str(n)), input("output file name?"))
