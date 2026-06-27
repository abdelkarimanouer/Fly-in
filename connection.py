class Connection:
    """Represents a road between two zones with a drone capacity limit."""

    def __init__(self, name1: str, name2: str,
                 max_link_capacity: int = 1) -> None:
        """Set up a connection between two zones."""

        self.name1: str = name1
        self.name2: str = name2
        self.max_link_capacity: int = max_link_capacity
        self.nb_drs_on_con: int = 0
