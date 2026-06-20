from dijkstra import Dijkstra
from zone import Zone
from typing import List, Any
from graph import Graph
from drone import Drone
from rich import print
from webcolors import name_to_hex


class Simulation:

    @staticmethod
    def create_drones(start_zone: Zone, nb_drones: int) -> List[Drone]:
        drones: List[Drone] = []
        for n in range(1, nb_drones + 1):
            d = Drone(n, start_zone, [])
            drones.append(d)
        return drones

    @staticmethod
    def assign_paths(graph: Graph) -> List[List[Zone]]:
        paths: List[List[Zone]] = []
        zone_type: str = ""

        best_path: List[Zone] = Dijkstra.shortest_path(graph)
        paths.append(best_path)

        for z in best_path:
            if z.hub_category == "start_hub" or z.hub_category == "end_hub":
                continue
            zone_type = z.zone_type
            z.zone_type = "blocked"
            try:
                best_path = Dijkstra.shortest_path(graph)
                if best_path not in paths:
                    paths.append(best_path)
            except Exception:
                continue
            finally:
                z.zone_type = zone_type
        return paths

    @staticmethod
    def path_of_drone(drones: List[Drone], paths: List[List[Zone]]) -> None:
        l_paths = len(paths)
        for d in drones:
            d.path = paths[d.id % l_paths]

    @staticmethod
    def _get_color(color: str | None) -> Any:
        if color is None:
            return "white"
        if color == "rainbow":
            return "magenta"
        return name_to_hex(color)

    @staticmethod
    def _print_turn(moved_drones: List[Drone]) -> None:
        rs = " ".join(f"D{d.id}-{d.log_output}" for d in moved_drones)
        print(rs)

    @staticmethod
    def start_simulation(graph: Graph, drones: List[Drone]) -> None:
        graph.start_zone.current_drones_on_zone = graph.nb_drones
        graph.end_zone.max_drones = graph.nb_drones
        while not all(
            d.cur_z.hub_category == "end_hub" for d in drones
        ):
            moved_drones: List[Drone] = []

            for d in drones:
                if d.cur_z.hub_category == "end_hub":
                    continue
                if d.turns_to_wait > 0:
                    d.turns_to_wait -= 1
                    if d.turns_to_wait == 0:
                        if d.destination_zone is not None:
                            d.cur_z = d.destination_zone
                        d.cur_z.current_drones_on_zone += 1
                        c1 = Simulation._get_color(d.cur_z.color)
                        d.log_output = f"[{c1}]{d.cur_z.name}[/{c1}]"
                        moved_drones.append(d)
                    continue
                n_z = d.path[d.d_pos_path]
                for c in graph.connections:
                    if {c.name1, c.name2} == {d.cur_z.name, n_z.name}:
                        if (
                            c.nb_drs_on_con < c.max_link_capacity
                            and n_z.current_drones_on_zone < n_z.max_drones
                        ):
                            if n_z.zone_type == "restricted":
                                d.cur_z.current_drones_on_zone -= 1
                                c.nb_drs_on_con += 1
                                d.turns_to_wait = 1
                                d.destination_zone = n_z
                                d.d_pos_path += 1
                                c1 = Simulation._get_color(d.cur_z.color)
                                c2 = Simulation._get_color(n_z.color)
                                d.log_output = f"[{c1}]{d.cur_z.name}\
[/{c1}]-[{c2}]{n_z.name}[/{c2}]"
                                moved_drones.append(d)
                            else:
                                d.cur_z.current_drones_on_zone -= 1
                                n_z.current_drones_on_zone += 1
                                c.nb_drs_on_con += 1
                                d.cur_z = n_z
                                d.d_pos_path += 1
                                c1 = Simulation._get_color(d.cur_z.color)
                                d.log_output = f"[{c1}]{d.cur_z.name}[/{c1}]"
                                moved_drones.append(d)
                        break

            for c in graph.connections:
                c.nb_drs_on_con = 0

            Simulation._print_turn(moved_drones)
