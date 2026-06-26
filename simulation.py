
from typing import List, Dict, Any
from webcolors import name_to_hex
from rich import print
from zone import Zone
from graph import Graph
from drone import Drone
from dijkstra import Dijkstra


class Simulation:
    @staticmethod
    def assign_path(graph: Graph) -> List[List[Zone]]:
        all_paths: List[List[Zone]] = []

        zone_drones: Dict = {z.name: 0 for z in graph.zones}

        original_zone_types: Dict = {z.name: z.zone_type for z in graph.zones}

        for d in range(1, graph.nb_drones + 1):
            try:
                best_path = Dijkstra.shortest_path(graph)
                all_paths.append(best_path)

                for zone in best_path:
                    if zone.hub_category not in ["start_hub", "end_hub"]:
                        zone_drones[zone.name] += 1

                        if zone_drones[zone.name] >= zone.max_drones:
                            zone.zone_type = "restricted"
            except ValueError:
                print(f"[ERROR]: No alternative path found for Drone {d}!")
                exit()

        for zone in graph.zones:
            zone.zone_type = original_zone_types[zone.name]

        return all_paths

    @staticmethod
    def _get_hex_color(color_name: str | None) -> Any:
        """
        The magic paintbrush! It turns color names into computer hex codes.
        """
        if not color_name:
            return "#ffffff"
        try:
            return name_to_hex(color_name.strip().lower())
        except ValueError:
            return "#ffffff"

    @staticmethod
    def _print_simulation(moves: List[Dict[str, Any]]) -> None:
        """
        The game announcer! It shouts out what all the drones did this turn.
        """
        line_parts: List[str] = []

        for move in moves:
            move_type = move["type"]
            drone_id = move["id"]

            if move_type == "normal":
                color_hex = Simulation._get_hex_color(move["color"])
                text = f"D{drone_id}-[{color_hex}]{move['zone_name']}[/]"
                line_parts.append(f"{text}")

            elif move_type == "connection":
                c1 = Simulation._get_hex_color(move["color_prev"])
                c2 = Simulation._get_hex_color(move["color_next"])
                prev_zone = f"[{c1}]{move['prev_zone']}[/{c1}]"
                next_zone = f"[{c2}]{move['next_zone']}[/{c2}]"
                text = f"D{drone_id}-{prev_zone}-{next_zone}"
                line_parts.append(f"{text}")

        if line_parts:
            print(" ".join(line_parts))

    @staticmethod
    def _calculate_occupancy(graph: Graph,
                             drones: List[Drone]) -> Dict[str, int]:
        """
        The parking lot helper. It counts how
        many drones are parked in each zone.
        """
        zone_occupancy = {z.name: 0 for z in graph.zones}

        for d in drones:
            if not d.is_done:
                if d.turns_to_wait == 1 and d.destination_zone:
                    zone_occupancy[d.destination_zone.name] += 1
                elif d.turns_to_wait == 0:
                    zone_occupancy[d.cur_z.name] += 1

        return zone_occupancy

    @staticmethod
    def start_simulation(graph: Graph, drones: List[Drone]) -> None:
        """
        The Main Game Loop! It runs turn-by-turn until everyone wins.
        """
        total_turns: int = 0

        while not all(d.is_done for d in drones):
            turn_moves: List[Dict[str, Any]] = []

            zone_occupancy = Simulation._calculate_occupancy(graph, drones)

            road_usage: Dict[str, int] = {}

            for d in drones:
                if d.is_done:
                    continue

                if d.turns_to_wait == 1 and d.destination_zone:
                    turn_moves.append({
                        "type": "normal",
                        "id": d.id,
                        "zone_name": d.destination_zone.name,
                        "color": d.destination_zone.color
                    })
                    d.cur_z = d.destination_zone
                    d.d_pos_path += 1
                    d.turns_to_wait = 0
                    d.destination_zone = None

                    if d.cur_z.hub_category == "end_hub":
                        d.is_done = True

                elif d.turns_to_wait == 0:
                    if d.d_pos_path >= len(d.path):
                        d.is_done = True
                        continue

                    next_zone = d.path[d.d_pos_path]
                    road_name = f"{d.cur_z.name}-{next_zone.name}"
                    max_road_space = 1

                    for conn in graph.connections:
                        if (conn.name1 == d.cur_z.name and conn.name2
                            == next_zone.name) or \
                           (conn.name2 == d.cur_z.name and conn.name1
                                == next_zone.name):
                            max_road_space = conn.max_link_capacity
                            break

                    zone_has_space = (next_zone.hub_category == "end_hub" or
                                      zone_occupancy[next_zone.name]
                                      < next_zone.max_drones)

                    road_has_space = (road_usage.get(road_name, 0)
                                      < max_road_space)

                    if zone_has_space and road_has_space:
                        road_usage[road_name] = road_usage.get(road_name, 0)+1

                        if d.cur_z.hub_category != "start_hub":
                            zone_occupancy[d.cur_z.name] -= 1

                        if next_zone.zone_type == "restricted":
                            d.turns_to_wait = 1
                            d.destination_zone = next_zone

                            turn_moves.append({
                                "type": "connection",
                                "id": d.id,
                                "prev_zone": d.cur_z.name,
                                "next_zone": next_zone.name,
                                "color_prev": d.cur_z.color,
                                "color_next": next_zone.color
                            })
                            if next_zone.hub_category != "end_hub":
                                zone_occupancy[next_zone.name] += 1

                        else:
                            turn_moves.append({
                                "type": "normal",
                                "id": d.id,
                                "zone_name": next_zone.name,
                                "color": next_zone.color
                            })
                            d.cur_z = next_zone
                            d.d_pos_path += 1

                            if next_zone.hub_category != "end_hub":
                                zone_occupancy[next_zone.name] += 1
                            if d.cur_z.hub_category == "end_hub":
                                d.is_done = True

            if turn_moves:
                total_turns += 1
                Simulation._print_simulation(turn_moves)

        print(f"\n[bold green]Simulation complete! "
              f"Total Turns: {total_turns}[/]")
