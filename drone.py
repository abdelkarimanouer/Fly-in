from typing import List
from zone import Zone


class Drone:
    def __init__(self, id: int, current_zone: Zone, path: List[Zone]):
        self.id: int = id
        self.current_zone: Zone = current_zone
        self.path: List[Zone] = path
        self.d_pos_path: int = 1
        self.is_done: bool = False
        self.turns_to_wait: int = 0
        self.destination_zone: Zone | None = None
        self.log_output: str = ""
