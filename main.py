from parsing import Parsing
from sys import argv
from graph import Graph
from simulation import Simulation


def main() -> None:
    if len(argv) < 2:
        raise ValueError("[ERROR]: No input file specified")

    parsing: Parsing = Parsing()
    graph: Graph = parsing.parsing_file(argv[1])

    paths = Simulation.assign_paths(graph)
    drones = Simulation.create_drones(graph.start_zone, graph.nb_drones)
    Simulation.path_of_drone(drones, paths)
    Simulation.start_simulation(graph, drones)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        exit()
