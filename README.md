*This project has been created as part of the 42 curriculum by aanouer.*

# Fly-in

## Description

A drone routing simulation system. It moves a fleet of drones from a start zone to an end zone through a network of connected zones in the fewest possible turns. The system parses a map file, finds the best path for each drone using Dijkstra's algorithm, and runs the simulation turn by turn with colored terminal output.

## Instructions

**Install dependencies:**
```bash
make install
```

**Run the simulation:**
```bash
make run ARG=path/to/map_file
```

**Debug mode:**
```bash
make debug ARG=path/to/map_file
```

**Clean cache:**
```bash
make clean
```

**check mypy and flake8:**
```bash
make lint
```

## Algorithm

The pathfinding uses **Dijkstra's algorithm** with zone-type-based costs:

- `normal` → cost 1
- `restricted` → cost 2
- `priority` → cost 1 (preferred)
- `blocked` → skipped entirely

When priority neighbors exist, Dijkstra picks them first. Each drone gets its own path assigned before the simulation starts.

The simulation runs in discrete turns. Each turn, every drone tries to move to the next zone in its path. Movement is blocked if the zone or road is at full capacity. Drones heading to restricted zones take 2 turns and must complete the move — they can't wait mid-connection.

## Visual Representation

The terminal output uses **rich** for colored text. Each drone move is printed as `D<id>-<zone>` with the zone name colored using its defined color from the map file. For restricted zone transit, the output shows both the previous and next zone: `D<id>-<prev_zone>-<next_zone>`. This makes it easy to follow each drone's movement turn by turn.

## Resources

- [Learn Graph](https://youtu.be/7zZ-VhLOy6M?si=V6QtcrgwR9vJxFKn)
- [Learn Dijkstra](https://youtu.be/NpJqtN2X9Qw?si=A8wUIdnn4Pt85W5g)
- [Claude AI](https://claude.ai)

**AI usage:** Claude AI was used for assistance during the project to help understand concepts and fix issues.
