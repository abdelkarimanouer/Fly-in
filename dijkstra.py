from graph import Graph
from zone import Zone
from typing import List, Dict
import heapq as h
import math


def dijkstra(graph: Graph, start: Zone, end: Zone) -> List[Zone]:
    path: List = []
    heap: List = []
    visited = set()
    parents: Dict = {}
    costs: Dict = {}

    for z in graph.zones:
        costs[z.name] = math.inf
    costs[start.name] = 0
    h.heappush(heap, (0, start.name))

    while heap:
        current_cost, name_zone = h.heappop(heap)
        if name_zone in visited:
            continue
        visited.add(name_zone)

        if name_zone == end.name:
            z = graph.get_zone_from_zones_list(name_zone)
            path.append(z)
            while name_zone != start.name:
                z = graph.get_zone_from_zones_list(parents[name_zone])
                path.append(z)
                name_zone = parents[name_zone]
            path.reverse()
            return path

        for n in graph.get_neighbor_zone(name_zone):
            if n.zone_type == "blocked":
                continue
            if n.name not in visited:
                new_cost = current_cost + graph.get_zone_cost(n)
                if new_cost < costs[n.name]:
                    costs[n.name] = new_cost
                    parents[n.name] = name_zone
                    h.heappush(heap, (new_cost, n.name))

    print("[ERROR]: No path found from start to end")
    exit()
