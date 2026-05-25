from graph import Graph
from connection import Connection
from zone import Zone
from typing import List, Dict


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


def parse_metadata(meta_data, line_num) -> Dict:
    default_data = {'color': None, 'zone_type': "normal",
                    'max_drones': 1
                    }
    if not meta_data:
        return default_data
    parts = ''.join(d + " " for d in meta_data)
    parts = parts.strip("[] ")
    if not parts:
        return default_data
    data_parts = parts.split()
    for d in data_parts:
        if "=" in d:
            meta = d.split("=")
            if len(meta) < 2:
                print("[ERROR]: metadata should be like this data=value")
                exit()
            data = meta[0]
            value = meta[1]
            if not value or not data:
                print(f"[ERROR] line <{line_num}>: metadata data|value"
                      f" cannot be empty")
                exit()
            if data == "color":
                default_data["color"] = value
            elif data == "zone":
                default_data["zone_type"] = value
            elif data == "max_drones":
                try:
                    default_data["max_drones"] = int(value)
                except Exception:
                    print("[ERROR]: max_drones should be integer")
            else:
                print("[ERROR]: Invalid metadata")
                exit()
        else:
            print("[ERROR]: metadata should be like this data=value")
            exit()
    return default_data


def parse_hub(line: str, zones: List[Zone], hub_category: str,
              already_found: bool, line_num: int) -> None:
    if already_found:
        print("[ERROR]: duplicate line found")
        exit()
    data: List = line.split()
    if len(data) < 4:
        print(f"[ERROR]: some data is messing in line <{line_num}>")
        exit()
    name: str = data[1]
    try:
        x: int = int(data[2])
        y: int = int(data[3])
    except Exception:
        print("[ERROR]: coordinates must be integers")
        exit()
    metadata: dict = parse_metadata(data[4:], line_num)
    zone = Zone(hub_category, name, (x, y), metadata['color'],
                metadata['zone_type'], metadata['max_drones'])
    zones.append(zone)


def parsing_file(file_path: str) -> Graph:
    try:
        nb_drones: int = -1
        zones: List[Zone] = []
        connections: List[Connection] = []
        lines: List[str] = []
        start_hub_found: bool = False

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
                parse_hub(line, zones, "start_hub", start_hub_found, i)
                start_hub_found = True
            elif line.startswith("end_hub"):
                ...
            elif line.startswith("hub"):
                ...
            elif line.startswith("connection"):
                ...
            else:
                print(f"[ERROR] line <{i}>: invalid syntax")
        return Graph(nb_drones, zones, connections)
    except Exception as e:
        print("[ERROR]:", e)
        exit()
