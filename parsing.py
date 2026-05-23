from graph import Graph
from connection import Connection
from zone import Zone
from typing import List


def parsing_file(file_path: str) -> Graph:
    try:
        nb_drones: int = 0
        nb_drones_parsed = False
        zones: List[Zone] = []
        connections: List[Connection] = []
        lines: List[str] = []

        with open(file_path, 'r') as f:
            lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith("#") or len(line) == 0:
                continue
            if line.startswith("nb_drones"):
                if ": " in line:
                    s = line.split(": ")
                else:
                    s = line.split(":")
                nb_drones = int(s[1])
                if nb_drones <= 0:
                    nb_drones_parsed = False
                    print("The First Line Should Be nb_drones")
                    exit()
                else:
                    nb_drones_parsed = True
            elif not nb_drones_parsed:
                print("The First Line Should Be nb_drones")
                exit()
            elif line.startswith("start_hub"):
                ...
            elif line.startswith("end_hub"):
                ...
            elif line.startswith("hub"):
                ...
            elif line.startswith("connection"):
                ...
            else:
                ...
        return Graph(nb_drones, zones, connections)
    except Exception as e:
        print("[ERROR]:", e)
        exit()
