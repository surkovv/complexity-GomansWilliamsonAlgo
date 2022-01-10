import scipy.stats as sps
import string

class Literal:
    def __init__(self, letter, neg):
        self.letter = letter
        self.neg = neg

    @classmethod
    def from_string(cls, string):
        if string[-1] == '*':
            return Literal(string[:-1], True)
        return Literal(string, False)

    def __str__(self):
        if self.neg:
            return self.letter + "*"
        else:
            return self.letter

    def negate(self):
        return Literal(self.letter, not self.neg)


class TwoCNF:
    def __init__(self):
        # Список кортежей из двух литералов
        self.disjunctions = []

    def add(self, disjunction):
        self.disjunctions.append(disjunction)

    def add_str(self, val1, val2):
        self.add((Literal.from_string(val1),
                  Literal.from_string(val2)))

    def __getitem__(self, item):
        return self.disjunctions[item]

    def num_feasible(self, values):
        result = 0
        for l1, l2 in self.disjunctions:
            if (l1.neg ^ values[l1.letter]) or (l2.neg ^ values[l2.letter]):
                result += 1
        return result

    @property
    def letters(self):
        result = set()
        for l1, l2 in self.disjunctions:
            result.add(l1.letter)
            result.add(l2.letter)
        return list(result)

    @classmethod
    def random_formula(cls, n_letters, n_disjunctions):
        result = TwoCNF()
        numbers = sps.randint(0, n_letters).rvs(n_disjunctions * 2)
        negs = sps.bernoulli(p=0.5).rvs(n_disjunctions * 2)
        for i in range(n_disjunctions):
            l1 = string.ascii_lowercase[numbers[i + i]]
            l2 = string.ascii_lowercase[numbers[i + i + 1]]
            if negs[i + i]:
                l1 += '*'
            if negs[i + i + 1]:
                l2 += '*'
            result.add_str(l1, l2)

        return result

    @classmethod
    def random_formula_feasible(cls, n_letters, n_disjunctions):
        result = TwoCNF()

        values = sps.bernoulli(p=0.5).rvs(n_letters)
        numbers = sps.randint(0, n_letters).rvs(n_disjunctions * 2)
        negs = sps.bernoulli(p=0.5).rvs(n_disjunctions * 2)
        for i in range(n_disjunctions):
            l1 = string.ascii_lowercase[numbers[i + i]]
            l2 = string.ascii_lowercase[numbers[i + i + 1]]
            if negs[i + i]:
                l1 += '*'
            if negs[i + i + 1]:
                l2 += '*'

            if not (negs[i + i] ^ values[numbers[i + i]]) \
                    and not (negs[i + i + 1] ^ values[numbers[i + i + 1]]):
                if len(l2) == 2:
                    l2 = l2[0]
                else:
                    l2 = l2 + '*'
            result.add_str(l1, l2)

        return result