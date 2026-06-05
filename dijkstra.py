from graph import Graph
from zone import Zone
from typing import List
import heapq as h
import math


def dijkstra(graph: Graph, start: Zone, end: Zone) -> List[Zone]:
    path = []
    heap = []
    visited = set()
    parents = {}
    costs = {}

    for z in graph.zones:
        costs[z.name] = math.inf
    costs[start.name] = 0
    h.heappush(heap, (0, start.name))

    return path
