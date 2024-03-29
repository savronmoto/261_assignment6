# Course: 261
# Author: Savanna Hanson
# Assignment: 5 - Graph Implementation
# Description: An directed graph ADT with vertices and edges stored as an adjacency matrix.
# Methods include add_vertex, add_edge, remove_edge, get_vertices, get_edges, is_valid_path,
# dfs, bfs, has_cycle, and dijksta.


import heapq
from collections import deque


class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        Adds a new vertex to the graph, by increasing the adjacency matrix by 1.
        Default weight is 0, and v_count is incremented.
        """

        self.v_count += 1

        for list in self.adj_matrix:
            list.append(0)
        new = []
        for _ in range(self.v_count):
            new.append(0)

        self.adj_matrix.append(new)

        return self.v_count


    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Adds an edge to the graph. Returns none if either of the vertices do not
        exist in the graph, or if the weight is not a positive integer, or if the src
        and dst are the same vertex. If the edge is already present, the weight is updated.
        """
        if src > self.v_count - 1 or dst > self.v_count - 1:
            return
        if weight < 1:
            return
        if src == dst:
            return

        self.adj_matrix[src][dst] = weight


    def remove_edge(self, src: int, dst: int) -> None:
        """
        Removes an edge between two vertices. If either (or both) vertex indices do not exist in the graph,
        or if there is no edge between them, the method does nothing.
        """
        if src > self.v_count - 1 or src < 0 or dst > self.v_count - 1 or dst < 0:
            return

        self.adj_matrix[src][dst] = 0

    def get_vertices(self) -> []:
        """
        Returns a list of the vertices in the graph.
        """
        vertices = []
        for list in range(self.v_count):
            vertices.append(list)
        return vertices

    def get_edges(self) -> []:
        """
        Returns a list of edges in the graph. Each edge is returned as a tuple of two
        incident vertex indices and weight. 1st element in tuple = source, 2nd = destination,
        3rd = weight. List is not ordered.
        """
        edges = []
        for i in range(self.v_count):
            lst = self.adj_matrix[i]
            for x in range(len(lst)):
                v = lst[x]
                if v != 0:
                    edges.append((i, x, v))

        return edges

    def is_valid_path(self, path: []) -> bool:
        """
        Takes a list of vertex indices and returns True if the sequence of vertices
        represents a valid path in the graph. Empty path is considered valid.
        """
        # Edge cases
        if len(path) == 0:
            return True
        if len(path) == 1:
            if path[0] < self.v_count:
                return True
            else:
                return False
        if len(path) == 2:
            if self.adj_matrix[path[0]][path[1]] != 0:
                return True
            else:
                return False

        j = 0
        while j < len(path) - 1:
            i = j
            j += 1
            src = path[i]
            dst = path[j]
            if self.adj_matrix[src][dst] == 0:
                return False
        return True


    def dfs(self, v_start, v_end=None) -> []:
        """
        Performs a depth-first search (DFS) in the graph and returns a list of vertices
        visited during the search, in the order they were visited.
        """

        if v_start > self.v_count - 1:
            return []

        # for key in self.adj_list:
        #     self.adj_list[key].sort(reverse=True)

        visited_vertices = []
        stack = deque()

        # add first vertex
        stack.append(v_start)

        while len(stack) != 0:
            v = stack.pop()
            if v_end:
                if v == v_end:
                    visited_vertices.append(v)
                    return visited_vertices
            if v not in visited_vertices:
                visited_vertices.append(v)
                temp = []
                for i in range(len(self.adj_matrix[v])):
                    ele = self.adj_matrix[v][i]
                    if ele != 0:
                        temp.append(i)
                temp.sort(reverse=True)
                for i in temp:
                    stack.append(i)
        return visited_vertices

    def bfs(self, v_start, v_end=None) -> []:
        """
        Performs a breadth-first search (BFS) in the graph and returns a list of vertices
        visited during the search, in the order they were visited.
        """

        if v_start > self.v_count - 1:
            return []

        # for key in self.adj_list:
        #     self.adj_list[key].sort(reverse=True)

        visited_vertices = []
        queue = deque()

        # add first vertex
        queue.append(v_start)

        while len(queue) != 0:
            v = queue.popleft()
            if v_end:
                if v == v_end:
                    visited_vertices.append(v)
                    return visited_vertices
            if v not in visited_vertices:
                visited_vertices.append(v)
            temp = []
            for i in range(len(self.adj_matrix[v])):
                ele = self.adj_matrix[v][i]
                if ele != 0:
                    temp.append(i)
                # temp.sort()
                for i in temp:
                    if i not in visited_vertices:
                        queue.append(i)

        return visited_vertices

    def has_cycle_helper(self, v, visited, recStack):
        """
        Recursive helper for has_cycle method. Creates
        Depth First Trees for each vertex in the graph to
        find back edges, which indicates a cycle.
        """
        visited[v] = True
        recStack[v] = True

        for index in range(len(self.adj_matrix[v])):
            # if a neighbor is visited and in recStack
            # then there is a cycle.
            neighbor = self.adj_matrix[v][index]
            if neighbor != 0:
                if not visited[index]:
                    if self.has_cycle_helper(index, visited, recStack) == True:
                        return True
                elif recStack[index] == True:
                    return True

        recStack[v] = False
        return False


    def has_cycle(self):
        """
        Determines if a graph (self) has a cycle. If graph is
        cyclic, returns True, if acyclic, returns False.
        Modified from https://www.geeksforgeeks.org/detect-cycle-in-a-graph/
        """

        # mark all the vertices as not visited
        visited = [False] * self.v_count
        recStack = [False] * self.v_count

        for i in range(self.v_count):
            if not visited[i]:
                if self.has_cycle_helper(i, visited, recStack):
                    return True

        return False


    def dijkstra(self, src: int) -> []:
        """
        Finds the shortest path from a given vertex to all other vertices in the graph using the
        Dijkstra algorithm. It returns a list of values that correspond to each vertex in the graph, where
        the value at index 0 is the length of the shortest path from vertex SRC to vertex 0, and so on.
        If a certain vertex is not reachable from SRC, returned value is infinity.
        """

        visited_table = {}
        # key is the vertex v
        # value is th min distance d to vertex v

        # insert source v into empty priority queue
        # as a tuple of (distance(priority), vertex, previous)
        hq = []
        heapq.heappush(hq, (0, src, None))

        #
        while hq:
            # Remove the first element (a vertex) from the priority queue
            # and assign it to v. Let d be v’s distance (priority)
            (d, v, p) = heapq.heappop(hq)
            if v not in visited_table:
                visited_table[v] = (d,p)
                for i in range(len(self.adj_matrix[v])):
                    cost = self.adj_matrix[v][i]
                    if cost:
                        dist = d + cost
                        heapq.heappush(hq, (dist, i, v))

        shortest_path = []

        # for each vertex in the graph, call min_path function to find total distance
        for i in range(len(self.adj_matrix)):
            if i in visited_table:
                shortest_path.append(visited_table[i][0])
            else:
                shortest_path.append(float('inf'))


            # val = self.min_path(i,visited_table)
            # shortest_path.append(val)

        return shortest_path

    def min_path(self, index, vertex_dict):
        """helper method"""
        # base case - if the parent is None, stop
        if vertex_dict[index][1] is None:
            return index

        tup = vertex_dict[index]
        distance = tup[0]

        distance += self.min_path(tup[1],vertex_dict)

        return distance


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)

    g.remove_edge(0,1)
    print(g)


    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 12),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)


    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
