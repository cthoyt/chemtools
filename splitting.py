import itertools

def makeSplittingList(l):
    # input list of doubles as (number hydrogens, coupling constant in hz)
    # output list of doubles as (relative coordinate, peak height)
    # produces a first-order coupling tree centered at zero with ratios of heights

	splits = []
	for num_hydrogen, j in l:
		splits.extend(j for i in range(num_hydrogen))
	
	shifts = reduce(lambda shifts, j: list(itertools.chain(*[rangeList(shift - j / 2.0, shift + j / 2.0, j) for shift in shifts])), splits, [0])

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
	data = [test1, test2, test3, test4, test5, test6, test7]
	for test, result in data:
		assert makeSplittingList(test) == result

def rangeList(start, stop, step):
	l = []
	while start <= stop:
		l.append(start)
		start += step
	return l

def test_rangeList():
	test1 = (0, 3, 1, [0, 1, 2, 3])
	test2 = (-2.5, 2.5, 5, [-2.5, 2.5])
	test3 = (-7.5, 7.5, 5, [-7.5, -2.5, 2.5, 7.5])
	data = [test1, test2, test3]
	for start, stop, step, result in data:
		assert rangeList(start, stop, step) == result

test_rangeList()
test_makeSplittingList()
