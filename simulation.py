from graph import Graph
from zone import Zone
from typing import List
from drone import Drone
from dijkstra import shortest_path


def assign_paths(graph: Graph, start: Zone, end: Zone, nb_drones: int):
    drones: List[Drone] = []
    drone_id: int = 1
    remaining: int = nb_drones

    while remaining > 0:
        path: List[Zone] = shortest_path(graph, start, end)
        min_capacity = min(z.max_drones for z in path)
        drones_for_path = min(remaining, min_capacity)

        for i in range(drones_for_path):
            drone = Drone(drone_id, start, path)
            drones.append(drone)
            drone_id += 1

        for zone in path:
            zone.current_drones += drones_for_path

        remaining -= drones_for_path

    return drones


def simulation(graph: Graph, drones: List[Drone], end: Zone):
    turn = 1

    while not all(drone.is_done for drone in drones):
        movements = []

        for drone in drones:
            if drone.is_done:
                continue
            next_zone: Zone = drone.path[drone.d_pos_path]

            if next_zone.current_drones < next_zone.max_drones:
                drone.current_zone.current_drones -= 1
                next_zone.current_drones += 1
                drone.current_zone = next_zone
                drone.d_pos_path += 1
                movements.append(f"D{drone.id}-{next_zone.name}")

                if next_zone.name == end.name:
                    drone.is_done = True

        print(" ".join(movements))
        turn += 1
