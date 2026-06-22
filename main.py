from parsing import Parsing
from sys import argv
from graph import Graph
from simulation import Simulation
from drone import Drone


def main() -> None:
    if len(argv) < 2:
        raise ValueError("[ERROR]: No input file specified")

    parsing: Parsing = Parsing()
    graph: Graph = parsing.parsing_file(argv[1])

    drones = Drone.create_drones(graph.start_zone, graph.nb_drones)

    paths = Simulation.assign_paths(graph)
    Drone.path_of_drone(drones, paths)

    Simulation.start_simulation(graph, drones)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        exit()
