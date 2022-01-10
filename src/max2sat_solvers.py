import numpy as np
import cvxpy as cp
import scipy.stats as sps
import scipy as sp

from src.formula import *


def formMatrix(formula: TwoCNF):
    letters = formula.letters
    n = len(letters)

    positions = {letters[i]: i for i in range(n)}

    matrix = np.zeros((n + 1, n + 1))
    for l1, l2 in formula.disjunctions:
        pos1 = positions[l1.letter]
        pos2 = positions[l2.letter]

        dop1 = -1 if l1.neg else 1
        dop2 = -1 if l2.neg else 1
        dop3 = -1 if l1.neg ^ l2.neg else 1

        matrix[pos1, n] -= dop1
        matrix[n, pos1] -= dop1
        matrix[pos2, n] -= dop2
        matrix[n, pos2] -= dop2
        matrix[pos1, pos2] += dop3
        matrix[pos2, pos1] += dop3

    return matrix


def solveOnSphere(formula: TwoCNF):
    n = len(formula.letters) + 1
    matrix = formMatrix(formula)
    X = cp.Variable((n, n), symmetric=True)

    constraints = [X[i, i] == 1 for i in range(n)]
    constraints.append(X >> 0)

    func = cp.Minimize(cp.trace(X @ matrix))
    problem = cp.Problem(func, constraints)
    problem.solve()

    return problem.value, X.value


def solveMax2SAT(formula: TwoCNF):
    value, gram_matrix = solveOnSphere(formula)

    xs = sp.linalg.lu(gram_matrix)[2]

    return fromSphereToMax2SAT(formula, xs)


def fromSphereToMax2SAT(formula: TwoCNF, xs):
    letters = formula.letters
    n = len(letters)
    hyperplane = getRandomHyperplane(n + 1)
    prods = hyperplane @ xs

    values = {}
    for i in range(n):
        if prods[i] > 0 > prods[n] or prods[i] < 0 < prods[n]:
            values[letters[i]] = 0
        else:
            values[letters[i]] = 1

    return formula.num_feasible(values)


def getRandomHyperplane(n):
    x = sps.norm().rvs(n)
    return x / np.linalg.norm(x)


def multiLaunch(formula: TwoCNF, num_iters=1000):
    value, gram_matrix = solveOnSphere(formula)

    xs = sp.linalg.lu(gram_matrix)[2]

    return np.array([fromSphereToMax2SAT(formula, xs) for _ in range(num_iters)])


def preciseSolver(formula: TwoCNF):
    letters = formula.letters
    M = 1 << len(letters)
    max_size = 0
    for mask in range(M):
        values = {}
        for i in range(len(letters)):
            values[letters[i]] = (mask >> i) & 1
        max_size = max(max_size, formula.num_feasible(values))
    return max_size
