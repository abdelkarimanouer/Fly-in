from parsing import parsing_file
from sys import argv
from graph import Graph
from zone import Zone


def main() -> None:
    graph: Graph = parsing_file(argv[1])
    for z in graph.zones:
        if z.hub_category == "start_hub":
            start: Zone = z
        if z.hub_category == "end_hub":
            end: Zone = z


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        exit()
