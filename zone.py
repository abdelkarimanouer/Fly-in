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
