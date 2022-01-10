import numpy as np
import cvxpy as cp
import scipy.stats as sps
import scipy as sp

from src.graph import Graph


def solveOnSphere(graph: Graph):
    n = graph.size
    X = cp.Variable((n, n), symmetric=True)

    constraints = [X[i, i] == 1 for i in range(n)]
    constraints.append(X >> 0)

    func = cp.Minimize(cp.trace(X @ graph.matrix))
    problem = cp.Problem(func, constraints)
    problem.solve()

    return problem.value, X.value


def solveCut(graph: Graph):
    value, gram_matrix = solveOnSphere(graph)

    xs = sp.linalg.lu(gram_matrix)[2]

    return fromSphereToCut(graph, xs)


def fromSphereToCut(graph: Graph, xs):
    hyperplane = getRandomHyperplane(graph.size)
    prods = hyperplane @ xs
    edges = graph.edges

    result = 0

    for u, v in edges:
        if prods[u] > 0 > prods[v]:
            result += 1
        if prods[u] < 0 < prods[v]:
            result += 1

    return result


def getRandomHyperplane(n):
    x = sps.norm().rvs(n)
    return x / np.linalg.norm(x)


def multiLaunch(graph: Graph, num_iters=1000):
    value, gram_matrix = solveOnSphere(graph)

    xs = sp.linalg.lu(gram_matrix)[2]

    return np.array([fromSphereToCut(graph, xs) for _ in range(num_iters)])


def preciseCut(graph: Graph):
    M = 1 << graph.size
    max_size = 0
    for mask in range(M):
        tmp = 0
        for a, b in graph.edges:
            ga = (mask >> a) & 1
            gb = (mask >> b) & 1
            tmp += (ga != gb)
        max_size = max(max_size, tmp)
    return max_size
