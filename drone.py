from typing import List
from zone import Zone


class Drone:
    """A drone that moves through zones to reach the end."""

    def __init__(self, id: int, current_zone: Zone, path: List[Zone]):
        """Set up a new drone with its starting zone and empty path."""

        self.id: int = id
        self.cur_z: Zone = current_zone
        self.path: List[Zone] = path
        self.d_pos_path: int = 1
        self.is_done: bool = False
        self.turns_to_wait: int = 0
        self.destination_zone: Zone | None = None
        self.log_output: str = ""

    @staticmethod
    def create_drones(start_zone: Zone, nb_drones: int) -> List["Drone"]:
        """Create a list of drones all starting at the same zone."""

        drones: List[Drone] = []
        for n in range(1, nb_drones + 1):
            d = Drone(n, start_zone, [])
            drones.append(d)
        return drones

    @staticmethod
    def path_drone(drones: List["Drone"], all_paths: List[List[Zone]]) -> None:
        """Assign a path to each drone."""

        l_paths = len(all_paths)
        for i in range(len(drones)):
            drones[i].path = all_paths[i % l_paths]
