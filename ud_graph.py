# Course: 261
# Author: Savanna Hanson
# Assignment: 5 - graphs
# Description:

from collections import deque

class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Add new vertex to the graph
        """
        if v in self.adj_list:
            return None

        self.adj_list[v] = []


    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph
        """
        if u == v:
            return

        # add vertices if needed
        if u not in self.adj_list:
            self.add_vertex(u)
        if v not in self.adj_list:
            self.add_vertex(v)

        # add edges
        if v not in self.adj_list[u]:
            self.adj_list[u].append(v)
        if u not in self.adj_list[v]:
            self.adj_list[v].append(u)

    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph
        """
        if v in self.adj_list and u in self.adj_list:
            self.adj_list[v].remove(u)
            self.adj_list[u].remove(v)
        else:
            return None


    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """
        if v in self.adj_list:
            # delete instances of vertex v in other lists
            for i in self.adj_list:
                if v in self.adj_list[i]:
                    self.adj_list[i].remove(v)
            # delete vertex v
            del self.adj_list[v]
        else:
            return None

    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """
        return list(self.adj_list)

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        dic = self.adj_list

        newlist = []
        visited_keys = []
        for key in dic:
            visited_keys.append(key)
            for v in dic[key]:
                if v not in visited_keys:
                    newlist.append((key,v))

        return newlist

    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """
        if path == []:
            return True

        if len(path) == 1 and path[0] in self.adj_list:
            return True
        if len(path) == 1 and path[0] not in self.adj_list:
            return False

        dic = self.adj_list
        i = 1
        k = 0
        keys = self.get_vertices()

        for v in range(len(path) - 1):
            key = keys[k]
            if path[i] not in dic[key]:
                return False
            i += 1
            k += 1
        return True


    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """
        if v_start not in self.adj_list:
            return []

        for key in self.adj_list:
            self.adj_list[key].sort(reverse=True)

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
                for successor in self.adj_list[v]:
                    stack.append(successor)

        return visited_vertices


    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """
        if v_start not in self.adj_list:
            return []

        for key in self.adj_list:
            self.adj_list[key].sort()

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
            for successor in self.adj_list[v]:
                if successor not in visited_vertices:
                    queue.append(successor)

        return visited_vertices

    def count_connected_components(self):
        """
        Return number of connected components in the graph
        Modified from https://www.geeksforgeeks.org/connected-components-in-an-undirected-graph/
        to meet assignment specs.
        """
        visited = {}
        cc = []

        # mark all the vertices as not visited
        for key in self.adj_list:
            visited[key] = False

        for v in self.adj_list:
            if not visited[v]:
                temp = []
                cc.append(self.dfs_helper(temp, v, visited))

        return len(cc)


    def dfs_helper(self, temp, v, visited):
        """Helper for connected components"""
        visited[v] = True

        temp.append(v)

        for i in self.adj_list[v]:
            if not visited[i]:
                temp = self.dfs_helper(temp, i, visited)
        return temp


    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        Modified from https://www.geeksforgeeks.org/detect-cycle-undirected-graph/
        """
        visited = {}

        # mark all the vertices as not visited
        for key in self.adj_list:
            visited[key] = False

        # Call the recursive helper function to detect cycle
        for i in self.adj_list:
            if not visited[i]:
                if self.has_cycle_helper(i, visited, -1) is True:
                    return True

        return False

    def has_cycle_helper(self, v, visited, parent):

        # Mark the current node as visited
        visited[v] = True

        for i in self.adj_list[v]:
            if not visited[i]:
                if self.has_cycle_helper(i, visited, v):
                    return True
            # If an adjacent vertex is visited and not parent of current vertex,
            # then there is a cycle
            elif parent != i:
                return True

        return False


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)

    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)

    print('\nremove sav edition')
    g = UndirectedGraph(['KB', 'KE', 'BK', 'BG', 'EG', 'EC', 'EI', 'EK', 'CJ'])
    print(g)
    g.remove_edge('r','E')
    print(g)


    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')

    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))

    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    print(g)
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')

    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()

    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
