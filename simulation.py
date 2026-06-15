from dijkstra import Dijkstra
from zone import Zone
from typing import List
from graph import Graph


class Simulation:

    @staticmethod
    def assign_paths(graph: Graph) -> List[List[Zone]]:
        paths: List[List[Zone]] = []
        zone_type: str = ""

        best_path: List[Zone] = Dijkstra.shortest_path(graph)
        paths.append(best_path)

        for z in best_path:
            if (z.hub_category == "start_hub" or
                    z.hub_category == "end_hub"):
                continue
            zone_type = z.zone_type
            z.zone_type = "blocked"
            try:
                best_path = Dijkstra.shortest_path(graph)
                if best_path not in paths:
                    paths.append(best_path)
            except Exception:
                continue
            finally:
                z.zone_type = zone_type
        return paths
