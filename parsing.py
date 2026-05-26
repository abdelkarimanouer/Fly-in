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


def parse_metadata_zones(meta_data: List[str], line_num: int) -> Dict:
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
                valid = ["normal", "blocked", "restricted", "priority"]
                if value not in valid:
                    print(f"[ERROR]: invalid zone type '{value}'")
                    exit()
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
    metadata: Dict = parse_metadata_zones(data[4:], line_num)
    zone = Zone(hub_category, name, (x, y), metadata['color'],
                metadata['zone_type'], metadata['max_drones'])

    for z in zones:
        if (z.name == zone.name) or (z.coordinate == zone.coordinate):
            print("[ERROR]: Every Zone should has unique name | coordinate")
            exit()
    zones.append(zone)


def parse_connection(line: str, connections: List[Connection],
                     zones: List[Zone], line_num: int) -> None:

    data = line.split()
    if data and len(data) > 1 and data[1]:

        names = data[1].split('-')
        if len(names) == 2:
            name1, name2 = names[0].strip(), names[1].strip()
            if not name1 or not name2:
                print("[ERROR]: One or both zones are empty")
                exit()
            name1_found = False
            name2_found = False
            for z in zones:
                if name1 == z.name:
                    name1_found = True
                if name2 == z.name:
                    name2_found = True
            if name1_found is False or name2_found is False:
                print("[ERROR]: One or both zones are empty")
                exit()
        else:
            print("[ERROR]: Invalid format. Expected connection "
                  "like this zone1-zone2.")
            exit()
        if len(data) > 2:
            if "=" in data[2]:
                data[2] = data[2].strip("[]")
                _, value = data[2].split("=")
                if not value:
                    print("[ERROR]: metadata should be like "
                          "this max_link_capacity=<value>")
                    exit()
                try:
                    v = int(value)
                except Exception:
                    print("[ERROR]: coordinates must be integers")
                    exit()
                connection = Connection(name1, name2, v)
            else:
                print("[ERROR]: metadata should be like "
                      "this max_link_capacity=<value>")
                exit()
        else:
            connection = Connection(name1, name2, 1)
        for c in connections:
            if (
                (connection.name1 == c.name1) and
                    (connection.name2 == c.name2) or
                    (connection.name1 == c.name2 and
                     connection.name2 == c.name1)):
                print("[ERROR]: connections should be unique")
                exit()
        connections.append(connection)
    else:
        print("[ERROR]: Data is missing or empty")
        exit()


def parsing_file(file_path: str) -> Graph:
    try:
        nb_drones: int = -1
        zones: List[Zone] = []
        connections: List[Connection] = []
        lines: List[str] = []
        nb_drones_found = False
        start_hub_found: bool = False
        end_hub_found: bool = False

        with open(file_path, 'r') as f:
            lines = f.readlines()
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if line.startswith("#") or len(line) == 0:
                continue
            if line.startswith("nb_drones"):
                if nb_drones_found:
                    print("[ERROR]: nb_drones should not be duplicated")
                    exit()
                nb_drones = get_nb_drones(line)
                if nb_drones == -1:
                    print("[ERROR]: nb_drones must be positive")
                    exit()
                nb_drones_found = True
            elif nb_drones == -1:
                print("[ERROR]: nb_drones must be the first line")
                exit()
            elif line.startswith("start_hub"):
                parse_hub(line, zones, "start_hub", start_hub_found, i)
                start_hub_found = True
            elif line.startswith("end_hub"):
                parse_hub(line, zones, "end_hub", end_hub_found, i)
                end_hub_found = True
            elif line.startswith("hub"):
                parse_hub(line, zones, "hub", False, i)
            elif line.startswith("connection"):
                parse_connection(line, connections, zones, i)
            else:
                print(f"[ERROR] line <{i}>: invalid syntax")
                exit()
        if not start_hub_found:
            print("[ERROR]: start_hub is missing")
            exit()
        if not end_hub_found:
            print("[ERROR]: end_hub is missing")
            exit()
        return Graph(nb_drones, zones, connections)
    except Exception as e:
        print("[ERROR]:", e)
        exit()
