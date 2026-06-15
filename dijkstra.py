from graph import Graph
from zone import Zone
from typing import List, Dict
import heapq as h
import math


class Dijkstra:

    @staticmethod
    def shortest_path(graph: Graph) -> List[Zone]:
        path: List = []
        heap: List = []
        visited = set()
        parents: Dict = {}
        costs: Dict = {}

        for z in graph.zones:
            costs[z] = math.inf
        costs[graph.start_zone] = 0
        h.heappush(heap, (0, graph.start_zone))

        while heap:
            current_cost, zone = h.heappop(heap)
            if zone in visited:
                continue
            visited.add(zone)

            if zone == graph.end_zone:
                path.append(zone)
                while zone != graph.start_zone:
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

        raise ValueError("[ERROR]: No path found from graph.start_zone to end")
