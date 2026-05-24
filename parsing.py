from graph import Graph
from connection import Connection
from zone import Zone
from typing import List


def get_nb_drones(line: str) -> int:
    nb_drones: int = 0

    if ": " in line:
        s = line.split(": ")
    else:
        s = line.split(":")
    nb_drones = int(s[1])
    if nb_drones <= 0:
        return -1
    else:
        return nb_drones


def parsing_file(file_path: str) -> Graph:
    try:
        nb_drones: int = -1
        zones: List[Zone] = []
        connections: List[Connection] = []
        lines: List[str] = []

        with open(file_path, 'r') as f:
            lines = f.readlines()
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if line.startswith("#") or len(line) == 0:
                continue
            if line.startswith("nb_drones"):
                nb_drones = get_nb_drones(line)
                if nb_drones == -1:
                    print("[ERROR]: nb_drones must be positive")
                    exit()
            elif nb_drones == -1:
                print("[ERROR]: nb_drones must be the first line")
                exit()
            elif line.startswith("start_hub"):
                line = line.replace(":", "")
            elif line.startswith("end_hub"):
                line = line.replace(":", "")
            elif line.startswith("hub"):
                line = line.replace(":", "")
            elif line.startswith("connection"):
                line = line.replace(":", "")
            else:
                print(f"[ERROR] line <{i}>: invalid syntax")
        return Graph(nb_drones, zones, connections)
    except Exception as e:
        print("[ERROR]:", e)
        exit()
