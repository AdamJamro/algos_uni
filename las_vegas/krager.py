import random
from itertools import combinations, combinations_with_replacement, permutations

import numpy as np

random.seed(21372137)

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n  # Tracks the number of remaining vertices/components

    def find(self, i):
        if (parent_i := self.parent[i]) == i:
            return i
        self.parent[i] = self.find(parent_i)
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i != root_j:
            if self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            elif self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            else:
                self.parent[root_j] = root_i
                self.rank[root_i] += 1
            self.count -= 1
            return True
        return False


def karger(num_vertices: int, edges):
    """
    Executes Karger's original algorithm contracting down to 2 vertices.
    :param num_vertices: Int, number of vertices (0 to num_vertices - 1)
    :param edges: List of tuples [(u, v), ...] representing undirected edges
    :return: Int, the size of the cut found in this run
    """
    if num_vertices <= 2:
        return 0

    uf = UnionFind(num_vertices)

    # Shuffle edges to allow a single linear pass for contraction
    shuffled_edges = np.array(list(edges))
    np.random.shuffle(shuffled_edges)
    assert shuffled_edges.shape[1] == 2

    # Contract edges linearly until 2 components remain
    edge_idx = 0
    while uf.count > 2 and edge_idx < len(shuffled_edges):
        u, v = shuffled_edges[edge_idx][0], shuffled_edges[edge_idx][1]
        uf.union(u, v)
        edge_idx += 1

    # Count the remaining edges between the two distinct components
    min_cut_edges_count = 0
    min_cut_edges = []
    for u, v in edges:
        if uf.find(u) != uf.find(v):
            min_cut_edges_count += 1
            min_cut_edges.append((u, v))

    return min_cut_edges_count, min_cut_edges


if __name__ == "__main__":
    # Example usage
    num_vertices = 8
    first_component = (list(permutations(range(4), 2)))
    second_component = (list(combinations(range(4, 8), 2)))
    connectors = [(1,4), (2,5)]

    edges = first_component + second_component + connectors

    mincut_size, mincut = karger(num_vertices, edges)

    tries = 3000
    times = []
    for time in range(tries):
        try_count = 1
        while karger(num_vertices, edges)[0] != 2:
            try_count += 1
        times.append(try_count)

    print(f"Average tries to find min cut: {np.mean(times)}")


    print(f"Example from a single run: Remaining vertices: {mincut_size}, Remaining edges: {mincut}")
