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
        # A big empty toy box to hold all our drones' secret maps
        all_paths: List[List[Zone]] = []
        
        # A notepad to count how many drones want to visit each parking lot
        zone_drones: Dict = {z.name: 0 for z in graph.zones}
        
        # Remember what the map looked like at the start before we change anything
        original_zone_types: Dict = {z.name: z.zone_type for z in graph.zones}

        # Look at every single drone, one by one (Drone 1, Drone 2...)
        for d in range(1, graph.nb_drones + 1):
            try:
                # Ask our magic pathfinder friend for the absolute fastest route!
                best_path = Dijkstra.shortest_path(graph)
                all_paths.append(best_path)

                # Look at every parking lot on this drone's new route
                for zone in best_path:
                    # If it's a real parking lot (not the start gate or finish line)
                    if zone.hub_category not in ["start_hub", "end_hub"]:
                        # Add 1 to our crowd counter for this parking lot
                        zone_drones[zone.name] += 1
                        
                        # Uh oh! If too many drones want to go here, it gets too crowded!
                        if zone_drones[zone.name] >= zone.max_drones:
                            # Change it to a slow "restricted" zone so future drones avoid it
                            zone.zone_type = "restricted"
            except ValueError:
                # If a drone gets completely trapped and can't find any path at all
                print(f"[ERROR]: No alternative path found for Drone {d}!")
                exit()

        # The planning is done! Change all the parking lots back to their normal original types
        for zone in graph.zones:
            zone.zone_type = original_zone_types[zone.name]

        # Give back the big box full of secret maps
        return all_paths

    @staticmethod
    def _get_hex_color(color_name: str | None) -> Any:
        """
        The magic paintbrush! It turns color names into computer hex codes.
        """
        # If there is no color name, just use standard white paint
        if not color_name:
            return "#ffffff"
        try:
            # Look up the color name in our big color dictionary
            return name_to_hex(color_name.strip().lower())
        except ValueError:
            # If it's a weird color name we don't know, just fall back to white
            return "#ffffff"

    @staticmethod
    def _print_simulation(moves: List[Dict[str, Any]]) -> None:
        """
        The game announcer! It shouts out what all the drones did this turn.
        """
        # A list to hold the words we want to print side-by-side
        line_parts: List[str] = []

        # Look at each drone's movement action for this turn
        for move in moves:
            move_type = move["type"]
            drone_id = move["id"]
            color_hex = Simulation._get_hex_color(move["color"])

            # If it's a normal instant hop to a regular zone
            if move_type == "normal":
                text = f"D{drone_id}-{move['zone_name']}"
                line_parts.append(f"[{color_hex}]{text}[/]")

            # If it's a slow 2-turn movement into a restricted zone
            elif move_type == "connection":
                text = f"D{drone_id}-{move['prev_zone']}-{move['next_zone']}"
                line_parts.append(f"[{color_hex}]{text}[/]")

        # If anyone moved, join all their text together and show it in full color!
        if line_parts:
            print(" ".join(line_parts))

    @staticmethod
    def _calculate_occupancy(graph: Graph,
                             drones: List[Drone]) -> Dict[str, int]:
        """
        The parking lot helper. It counts how many drones are parked in each zone.
        """
        # Start our notepad with 0 drones parked in every single zone
        zone_occupancy = {z.name: 0 for z in graph.zones}
        
        # Check every drone to see where it is sitting or landing
        for d in drones:
            # Skip drones that already finished the game and went home
            if not d.is_done:
                # If the drone is flying in the air and landing here this turn
                if d.turns_to_wait == 1 and d.destination_zone:
                    zone_occupancy[d.destination_zone.name] += 1
                # If the drone is already sitting stationary inside this zone
                elif d.turns_to_wait == 0:
                    zone_occupancy[d.cur_z.name] += 1
                    
        return zone_occupancy

    @staticmethod
    def start_simulation(graph: Graph, drones: List[Drone]) -> None:
        """
        The Main Game Loop! It runs turn-by-turn until everyone wins.
        """
        # Start our game clock at turn 0
        total_turns: int = 0

        # Keep playing the game as long as at least one drone is still flying
        while not all(d.is_done for d in drones):
            # A fresh empty list to collect all movements made in this single turn
            turn_moves: List[Dict[str, Any]] = []
            
            # Count how many drones are parked in each lot at the start of this turn
            zone_occupancy = Simulation._calculate_occupancy(graph, drones)

            # A fresh notepad to count how many drones are driving on each road *right now*
            road_usage: Dict[str, int] = {}

            # Look at every drone to let them make their choice for this turn
            for d in drones:
                # If this drone already reached the final goal, it skips its turn
                if d.is_done:
                    continue

                # --- CASE 1: The drone was flying mid-air and finally lands this turn! ---
                if d.turns_to_wait == 1 and d.destination_zone:
                    turn_moves.append({
                        "type": "normal",
                        "id": d.id,
                        "zone_name": d.destination_zone.name,
                        "color": d.destination_zone.color
                    })
                    # Update its current position to the new zone it just landed on
                    d.cur_z = d.destination_zone
                    d.d_pos_path += 1  # Move its map index forward
                    d.turns_to_wait = 0  # It landed, so it doesn't have to wait anymore
                    d.destination_zone = None  # Reset its destination helper

                    # If it just landed on the final goal trophy zone, it wins!
                    if d.cur_z.hub_category == "end_hub":
                        d.is_done = True

                # --- CASE 2: The drone is sitting still and wants to start a new move! ---
                elif d.turns_to_wait == 0:
                    # If the drone already completed all steps on its secret map
                    if d.d_pos_path >= len(d.path):
                        d.is_done = True
                        continue

                    # Look at its secret map to find out which zone it wants to go to next
                    next_zone = d.path[d.d_pos_path]

                    # Give this specific road a clean name (like "start-slow_path1")
                    road_name = f"{d.cur_z.name}-{next_zone.name}"
                    
                    # Look through our map rules to find this road's maximum capacity limit
                    max_road_space = 1
                    for conn in graph.connections:
                        if (conn.name1 == d.cur_z.name and conn.name2 == next_zone.name) or \
                           (conn.name2 == d.cur_z.name and conn.name1 == next_zone.name):
                            max_road_space = conn.max_link_capacity
                            break
                            
                    # Check if the parking lot has space (or if it's the magical un-dumpable end goal)
                    zone_has_space = (next_zone.hub_category == "end_hub" or 
                                      zone_occupancy[next_zone.name] < next_zone.max_drones)
                                      
                    # Check if our road notepad shows that this road still has open lanes
                    road_has_space = (road_usage.get(road_name, 0) < max_road_space)

                    # THE GOLDEN RULE: The drone can ONLY move if the lot AND the road have space!
                    if zone_has_space and road_has_space:
                        # Tell our notepad that 1 drone is taking up a lane on this road right now
                        road_usage[road_name] = road_usage.get(road_name, 0) + 1

                        # If it leaves a regular zone, free up 1 parking slot from that old zone
                        if d.cur_z.hub_category != "start_hub":
                            zone_occupancy[d.cur_z.name] -= 1

                        # SUB-CASE A: The next zone is a slow, restricted zone!
                        if next_zone.zone_type == "restricted":
                            d.turns_to_wait = 1  # Tell it that it must fly for 2 whole turns
                            d.destination_zone = next_zone  # Set its future landing spot

                            turn_moves.append({
                                "type": "connection",
                                "id": d.id,
                                "prev_zone": d.cur_z.name,
                                "next_zone": next_zone.name,
                                "color": next_zone.color
                            })
                            # Reserve its parking slot early so nobody steals it while it's flying
                            if next_zone.hub_category != "end_hub":
                                zone_occupancy[next_zone.name] += 1
                                
                        # SUB-CASE B: The next zone is a normal or priority fast zone!
                        else:
                            turn_moves.append({
                                "type": "normal",
                                "id": d.id,
                                "zone_name": next_zone.name,
                                "color": next_zone.color
                            })
                            # It slides right into the next zone instantly!
                            d.cur_z = next_zone
                            d.d_pos_path += 1

                            # Update the parking counter for the zone it just entered
                            if next_zone.hub_category != "end_hub":
                                zone_occupancy[next_zone.name] += 1
                            # If it reached the finish line instantly, it's done!
                            if d.cur_z.hub_category == "end_hub":
                                d.is_done = True

            # If any drone made a move or state change, finish the turn and count it!
            if turn_moves:
                total_turns += 1
                Simulation._print_simulation(turn_moves)

        # The loop finished because all drones are done! Print the final scoreboard.
        print(f"\n[bold green]Simulation complete! Total Turns: {total_turns}[/]")
