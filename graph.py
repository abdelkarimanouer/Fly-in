from typing import List
from zone import Zone
from connection import Connection


class Graph:
    def __init__(self, nb_drones: int, zones: List[Zone],
                 connections: List[Connection]) -> None:
        self.nb_drones: int = nb_drones
        self.zones: List[Zone] = zones
        self.connections: List[Connection] = connections
