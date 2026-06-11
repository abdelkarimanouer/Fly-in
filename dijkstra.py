from graph import Graph
from zone import Zone
from typing import List, Dict
import heapq as h
import math


class Dijkstra:

    def shortest_path(self, graph: Graph, start: Zone,
                      end: Zone) -> List[Zone]:
        path: List = []
        heap: List = []
        visited = set()
        parents: Dict = {}
        costs: Dict = {}

        for z in graph.zones:
            costs[z] = math.inf
        costs[start] = 0
        h.heappush(heap, (0, start))

        while heap:
            current_cost, zone = h.heappop(heap)
            if zone in visited:
                continue
            visited.add(zone)

            if zone == end:
                path.append(zone)
                while zone != start:
                    path.append(parents[zone])
                    zone = parents[zone]
                path.reverse()
                return path

            for n in graph.adjacency[zone]:
                if n.zone_type == "blocked":
                    continue
                new_cost = current_cost + n.get_zone_cost()
                if new_cost < costs[n]:
                    costs[n] = new_cost
                    parents[n] = zone
                    h.heappush(heap, (new_cost, n))

        raise ValueError("[ERROR]: No path found from start to end")
