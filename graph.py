from typing import List, Dict
from zone import Zone
from connection import Connection


class Graph:
    """Holds all zones, connections, and the adjacency map."""

    def __init__(self, nb_drones: int, zones: List[Zone],
                 connections: List[Connection]) -> None:
        """Build the graph from zones and connections."""

        self.nb_drones: int = nb_drones
        self.zones: List[Zone] = zones
        self.connections: List[Connection] = connections
        self.adjacency: Dict[Zone, List[Zone]] = {}
        self.start_zone: Zone
        self.end_zone: Zone
        self._get_start_end_zones()
        self._create_graph()

    def _get_start_end_zones(self) -> None:
        """Find and store the start and end zones."""

        for z in self.zones:
            if z.hub_category == "start_hub":
                z.max_drones = self.nb_drones
                self.start_zone = z
            if z.hub_category == "end_hub":
                z.max_drones = self.nb_drones
                self.end_zone = z

    def _create_graph(self) -> None:
        """Build the adjacency map from connections."""

        for z in self.zones:
            self.adjacency[z] = []
        for c in self.connections:
            zone1 = self.get_zone_from_zones_list(c.name1)
            zone2 = self.get_zone_from_zones_list(c.name2)
            self.adjacency[zone1].append(zone2)
            self.adjacency[zone2].append(zone1)

    def get_zone_from_zones_list(self, name: str) -> Zone:
        """Return the zone that matches the given name."""

        for z in self.zones:
            if z.name == name:
                return z
        raise ValueError(f"Zone '{name}' not found")
