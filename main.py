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
    for path in paths:
        print()
        print(path)
        print()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        exit()
