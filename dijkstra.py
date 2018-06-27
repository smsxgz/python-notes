# http://www.bogotobogo.com/python/python_Dijkstras_Shortest_Path_Algorithm.php

import math


class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
        # Set distance to infinity for all nodes
        self.distance = math.inf
        # Predecessor
        self.previous = None

    def add_neighbor(self, neighbor, weight):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_previous(self, prev):
        self.previous = prev

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str(
            [x.id for x in self.adjacent])


class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        return self.vert_dict.get(n)

    def add_edge(self, frm, to, cost):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)


def shortest(v, path):
    ''' make shortest path from v.previous'''
    if v.previous:
        path.append(v.previous.get_id())
        shortest(v.previous, path)
    return


import heapq


def dijkstra(aGraph, start, target):
    start.set_distance(0)

    # Put tuple pair into the priority queue
    visited = set()
    heap = [(0, start.get_id())]
    heapq.heapify(heap)

    while len(visited) < aGraph.num_vertices:
        # Pops a vertex with the smallest distance
        uv = heapq.heappop(heap)
        current = aGraph.get_vertex(uv[1])
        visited.add(uv[1])

        for next_vertex in current.adjacent:
            if next_vertex in visited:
                continue
            new_dist = current.get_distance() + current.get_weight(next_vertex)

            if new_dist < next_vertex.get_distance():
                next_vertex.set_distance(new_dist)
                next_vertex.set_previous(current)
                heapq.heappush(heap, (new_dist, next_vertex.get_id()))


if __name__ == '__main__':

    g = Graph()

    g.add_vertex('a')
    g.add_vertex('b')
    g.add_vertex('c')
    g.add_vertex('d')
    g.add_vertex('e')
    g.add_vertex('f')

    g.add_edge('a', 'b', 7)
    g.add_edge('a', 'c', 9)
    g.add_edge('a', 'f', 14)
    g.add_edge('b', 'c', 10)
    g.add_edge('b', 'd', 15)
    g.add_edge('c', 'd', 11)
    g.add_edge('c', 'f', 2)
    g.add_edge('d', 'e', 6)
    g.add_edge('e', 'f', 9)

    dijkstra(g, g.get_vertex('a'), g.get_vertex('e'))

    target = g.get_vertex('e')
    path = [target.get_id()]
    shortest(target, path)
    print('The shortest path : %s' % (path[::-1]))
