from typing import List
from zone import Zone


class Drone:
    def __init__(self, id: int, current_zone: Zone, path: List[Zone]):
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
        drones: List[Drone] = []
        for n in range(1, nb_drones + 1):
            d = Drone(n, start_zone, [])
            drones.append(d)
        return drones

    @staticmethod
    def path_of_drone(drones: List["Drone"], paths: List[List[Zone]]) -> None:
        l_paths = len(paths)
        if l_paths == 0:
            print("[ERROR]: No valid paths were found from \
start_hub to end_hub!")
            exit()

        for d in drones:
            d.path = paths[(d.id - 1) % l_paths]
