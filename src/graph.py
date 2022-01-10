import numpy as np
import scipy.stats as sps

class Graph:
    def __init__(self):
        self.size = 1
        self.matrix = np.zeros((1, 1))

    @classmethod
    def fromEdges(cls, size, edges):
        graph = Graph()
        graph.size = size
        graph.matrix = np.zeros((size, size))
        for u, v in edges:
            graph.matrix[u, v] = graph.matrix[v, u] = 1
        return graph

    @classmethod
    def randomGraph(cls, size, p):
        graph = Graph()
        graph.size = size
        graph.matrix = sps.bernoulli(p).rvs((size, size))
        graph.matrix[np.triu_indices(size)] = 0
        graph.matrix += graph.matrix.T

        return graph

    @classmethod
    def randomBiparite(cls, left, right, p):
        size = left + right
        graph = Graph()
        graph.size = size
        graph.matrix = sps.bernoulli(p).rvs((size, size))
        graph.matrix[np.triu_indices(size)] = 0
        graph.matrix += graph.matrix.T
        graph.matrix[:left, :left] = 0
        graph.matrix[left:, left:] = 0

        return graph

    @property
    def edges(self):
        e = []
        for u in range(self.size):
            for v in range(u + 1, self.size):
                if self.matrix[u, v]:
                    e.append((u, v))
        return e
