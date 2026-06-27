from parsing import Parsing
from sys import argv
from graph import Graph
from drone import Drone
from simulation import Simulation


def main() -> None:
    """Parse the map file, set up drones, and run the simulation."""

    if len(argv) < 2:
        raise ValueError("[ERROR]: No input file specified")

    parsing: Parsing = Parsing()
    graph: Graph = parsing.parsing_file(argv[1])

    drones = Drone.create_drones(graph.start_zone, graph.nb_drones)
    all_paths = Simulation.assign_path(graph)
    Drone.path_drone(drones, all_paths)

    Simulation.start_simulation(graph, drones)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("exit...")
        exit()
    except Exception as e:
        print(e)
        exit()
