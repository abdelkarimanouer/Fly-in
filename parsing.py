from graph import Graph
from connection import Connection
from zone import Zone
from typing import List, Dict


class Parsing:

    def _get_nb_drones(self, line: str, line_num: int) -> int:

        nb_drones: int = 0

        if ": " in line:
            s = line.split(": ")
        else:
            s = line.split(":")
        try:
            nb_drones = int(s[1])
        except Exception:
            print(f"[ERROR] line <{line_num}>: Invalid nb_drones "
                  f"(nb_drones: <number>)")
            exit()
        if nb_drones <= 0:
            return -1
        else:
            return nb_drones

    def _parse_metadata_zones(self, meta_data: List[str],
                              line_num: int) -> Dict:
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
                    print(f"[ERROR] line <{line_num}>: metadata should be "
                          f"like this data=value")
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
                        print(f"[ERROR] line <{line_num}>: "
                              f"invalid zone type '{value}'")
                        exit()
                    default_data["zone_type"] = value
                elif data == "max_drones":
                    try:
                        default_data["max_drones"] = int(value)
                    except Exception:
                        print(f"[ERROR] line <{line_num}>: "
                              f"max_drones should be integer")
                        exit()
                else:
                    print(f"[ERROR] line <{line_num}>: Invalid metadata")
                    exit()
            else:
                print(f"[ERROR] line <{line_num}>: metadata should be "
                      f"like this data=value")
                exit()
        return default_data

    def _parse_hub(self, line: str, zones: List[Zone], hub_category: str,
                   already_found: bool, line_num: int) -> None:
        if already_found:
            print(f"[ERROR] line <{line_num}>: duplicate line found")
            exit()
        data: List = line.split()
        if len(data) < 4:
            print(f"[ERROR] line <{line_num}>: some data is missing")
            exit()
        name: str = data[1]
        try:
            x: int = int(data[2])
            y: int = int(data[3])
        except Exception:
            print(f"[ERROR] line <{line_num}>: coordinates must be integers")
            exit()
        metadata: Dict = self._parse_metadata_zones(data[4:], line_num)
        zone = Zone(hub_category, name, (x, y), metadata['color'],
                    metadata['zone_type'], metadata['max_drones'])

        for z in zones:
            if (z.name == zone.name) or (z.coordinate == zone.coordinate):
                print(f"[ERROR] line <{line_num}>: Every Zone should "
                      f"have unique name | coordinate")
                exit()
        zones.append(zone)

    def _parse_connection(self, line: str, connections: List[Connection],
                          zones: List[Zone], line_num: int) -> None:

        data = line.split()
        if data and len(data) > 1 and data[1]:

            names = data[1].split('-')
            if len(names) == 2:
                name1, name2 = names[0].strip(), names[1].strip()
                if not name1 or not name2:
                    print(f"[ERROR] line <{line_num}>: One or "
                          f"both zones are empty")
                    exit()
                name1_found = False
                name2_found = False
                for z in zones:
                    if name1 == z.name:
                        name1_found = True
                    if name2 == z.name:
                        name2_found = True
                if name1_found is False or name2_found is False:
                    print(f"[ERROR] line <{line_num}>: One or both "
                          f"zones do not exist")
                    exit()
            else:
                print(f"[ERROR] line <{line_num}>: Invalid format. Expected "
                      f"connection: zone1-zone2")
                exit()
            if len(data) > 2:
                if "=" in data[2]:
                    data[2] = data[2].strip("[]")
                    _, value = data[2].split("=")
                    if not value:
                        print(f"[ERROR] line <{line_num}>: max_link_capacity "
                              f"value cannot be empty")
                        exit()
                    try:
                        v = int(value)
                    except Exception:
                        print(f"[ERROR] line <{line_num}>: max_link_capacity "
                              f"must be an integer")
                        exit()
                    connection = Connection(name1, name2, v)
                else:
                    print(f"[ERROR] line <{line_num}>: metadata should "
                          f"be like [max_link_capacity=value]")
                    exit()
            else:
                connection = Connection(name1, name2, 1)
            for c in connections:
                if (
                    (connection.name1 == c.name1) and
                    (connection.name2 == c.name2) or
                    (connection.name1 == c.name2 and
                     connection.name2 == c.name1)):
                    print(f"[ERROR] line <{line_num}>: duplicate "
                          f"connection found")
                    exit()
            connections.append(connection)
        else:
            print(f"[ERROR] line <{line_num}>: Connection data "
                  f"is missing or empty")
            exit()

    def parsing_file(self, file_path: str) -> Graph:
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
                        print(f"[ERROR] line <{i}>: nb_drones should "
                              f"not be duplicated")
                        exit()
                    nb_drones = self._get_nb_drones(line, i)
                    if nb_drones == -1:
                        print(f"[ERROR] line <{i}>: nb_drones "
                              f"must be positive")
                        exit()
                    nb_drones_found = True
                elif nb_drones == -1:
                    print(f"[ERROR] line <{i}>: nb_drones "
                          f"must be the first line")
                    exit()
                elif line.startswith("start_hub"):
                    self._parse_hub(line, zones, "start_hub",
                                    start_hub_found, i)
                    start_hub_found = True
                elif line.startswith("end_hub"):
                    self._parse_hub(line, zones, "end_hub",
                                    end_hub_found, i)
                    end_hub_found = True
                elif line.startswith("hub"):
                    self._parse_hub(line, zones, "hub", False, i)
                elif line.startswith("connection"):
                    self._parse_connection(line, connections, zones, i)
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

        except FileNotFoundError:
            print(f"[ERROR]: The map file '{file_path}' was not found")
            exit()
        except Exception as e:
            print(f"[ERROR]: System failure while reading file: {e}")
            exit()
