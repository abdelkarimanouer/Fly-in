from typing import Tuple


class Zone:
    def __init__(self, hub_category: str, name: str, coordinate: Tuple,
                 color: str | None = None, zone_type: str = "normal",
                 max_drones: int = 1) -> None:
        self.hub_category: str = hub_category
        self.name: str = name
        self.coordinate: Tuple = coordinate
        self.color: str | None = color
        self.zone_type: str = zone_type
        self.max_drones: int = max_drones
        self.current_drones: int = 0

    def __lt__(self, other) -> bool:
        return self.name < other.name

    def get_zone_cost(self) -> int:
        costs = {
            "normal": 1,
            "blocked": -1,
            "restricted": 2,
            "priority": 1
        }
        return costs.get(self.zone_type, 1)
