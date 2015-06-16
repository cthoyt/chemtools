__author__ = 'cthoyt'

"""
for now, a d-orbital will be represented as a dictionary

    key = angular momentum quantum number
    value = set representing the electrons contained in the orbital
            such that an electron with spin quantum number +1/2 is represented by true
            and an electron with -1/2 is represented by false
"""


class DOrbital(dict):
    def __init__(self, n_electrons):
        self.n_electrons = n_electrons
        assert 10 >= n_electrons
        if n_electrons <= 5:
            for n in range(2, 2 - n_electrons, -1):
                self[n] = {True}
        else:
            for n in range(-2, 3):
                self[n] = {True}
            for n in range(2, 2 - (n_electrons - 5), -1):
                self[n].add(False)

    def __str__(self):
        s = ""
        for key in sorted(self.keys(), reverse=True):
            s += "%+d" % key

            e = ""
            if True in self[key]:
                e += "↑"
            if False in self[key]:
                e += "↓"

            s += "%-2s " % e
        return s

    def calculate_ground_state(self):
        pass


print(repr(DOrbital(4)))
print(DOrbital(6))
