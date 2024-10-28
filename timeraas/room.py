class Room:
    def __init__(self, name: str, floor: int):
        self.name = name  # Setter will handle validation
        self.floor = floor  # Setter will handle validation

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Room name must be a non-empty string.")
        self._name = value

    @property
    def floor(self) -> int:
        return self._floor

    @floor.setter
    def floor(self, value: int):
        if not isinstance(value, int):
            raise ValueError("Floor must be an integer.")
        self._floor = value

    def __str__(self) -> str:
        return f"Room(name='{self.name}', floor={self.floor})"

    def __repr__(self) -> str:
        return f"Room(name={self.name!r}, floor={self.floor!r})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Room):
            return False
        return self.name == other.name and self.floor == other.floor

    def __hash__(self):
        return hash((self.name, self.floor))
