from graph import Graph
from connection import Connection
from zone import Zone
from typing import List


def parsing_file(file_path: str) -> Graph:
    nb_drones: int = 0
    zones: List[Zone] = []
    connections: List[Connection] = []
    return Graph(nb_drones, zones, connections)
