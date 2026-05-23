from graph import Graph
from connection import Connection
from zone import Zone
from typing import List


def parsing_file(file_path: str) -> Graph:
    nb_drones: int = 0
    zones: List[Zone] = []
    connections: List[Connection] = []
    lines: List[str] = []

    with open(file_path, 'r') as f:
        lines = f.readlines()
    for l in lines:
        l = l.strip()
        if l.startswith("#") or len(l) == 0:
            continue
        elif l.startswith("start_hub"):
            ...
        elif l.startswith("end_hub"):
            ...
        elif l.startswith("hub"):
            ...
        elif l.startswith("connection"):
            ...
        else:
            ...
        

    return Graph(nb_drones, zones, connections)
