from parsing import parsing_file
from sys import argv
from graph import Graph
from drone import Drone
from zone import Zone
from simulation import simulation, assign_paths
from typing import List


def main() -> None:
    graph: Graph = parsing_file(argv[1])
    for z in graph.zones:
        if z.hub_category == "start_hub":
            start: Zone = z
        if z.hub_category == "end_hub":
            end: Zone = z
    drones: List[Drone] = assign_paths(graph, start, end, graph.nb_drones)
    start.current_drones = graph.nb_drones
    simulation(graph, drones, end)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        exit()
