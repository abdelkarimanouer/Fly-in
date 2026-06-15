from typing import List, Dict
from zone import Zone
from connection import Connection


class Graph:
    def __init__(self, nb_drones: int, zones: List[Zone],
                 connections: List[Connection]) -> None:
        self.nb_drones: int = nb_drones
        self.zones: List[Zone] = zones
        self.connections: List[Connection] = connections
        self.adjacency: Dict[Zone, List[Zone]] = {}
        self.start_zone: Zone
        self.end_zone: Zone
        self._get_start_end_zones()
        self._create_graph()

    def _get_start_end_zones(self) -> None:
        for z in self.zones:
            if z.hub_category == "start_hub":
                self.start_zone = z
            if z.hub_category == "end_hub":
                self.end_zone = z

    def _create_graph(self) -> None:
        for z in self.zones:
            self.adjacency[z] = []
        for c in self.connections:
            zone1 = self.get_zone_from_zones_list(c.name1)
            zone2 = self.get_zone_from_zones_list(c.name2)
            self.adjacency[zone1].append(zone2)
            self.adjacency[zone2].append(zone1)

    def get_zone_from_zones_list(self, name: str) -> Zone:
        for z in self.zones:
            if z.name == name:
                return z
        raise ValueError(f"Zone '{name}' not found")
