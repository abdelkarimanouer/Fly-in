from typing import List
from zone import Zone
from connection import Connection


class Graph:
    def __init__(self, nb_drones: int, zones: List[Zone],
                 connections: List[Connection]) -> None:
        self.nb_drones: int = nb_drones
        self.zones: List[Zone] = zones
        self.connections: List[Connection] = connections

    def get_zone_from_zones_list(self, name: str) -> Zone:
        for z in self.zones:
            if z.name == name:
                return z
        raise ValueError(f"Zone '{name}' not found")

    def get_zone_cost(self, zone: Zone) -> int:
        costs = {
            "normal": 1,
            "blocked": -1,
            "restricted": 2,
            "priority": 1
        }
        return costs.get(zone.zone_type, 1)

    def get_neighbor_zone(self, name_zone: str) -> List[Zone]:
        try:
            neighbors: List[Zone] = []

            for c in self.connections:
                if name_zone == c.name1:
                    z = self.get_zone_from_zones_list(c.name2)
                    neighbors.append(z)
                if name_zone == c.name2:
                    z = self.get_zone_from_zones_list(c.name1)
                    neighbors.append(z)
            return neighbors
        except Exception as e:
            raise ValueError(str(e))
