from enum import Enum
from timeraas.room import Room


class WindowStatus(Enum):
    OPEN = 1
    TILTED = 2
    CLOSED = 3


class Window:
    def __init__(self, location: Room):
        self._location = location
        self._status = WindowStatus.CLOSED  # Store enum instance, not string

    @property
    def location(self) -> Room:
        """Read-only access to the room location of the window."""
        return self._location

    @property
    def status(self) -> WindowStatus:
        return self._status

    @status.setter
    def status(self, new_status):
        if isinstance(new_status, WindowStatus):
            self._status = new_status
        elif isinstance(new_status, str):
            # Allow string names for flexibility
            try:
                self._status = WindowStatus[new_status.upper()]
            except KeyError:
                raise ValueError(f"{new_status} is not a valid WindowStatus.")
        else:
            raise TypeError("Status must be a WindowStatus enum or valid status name as string.")

    def __str__(self) -> str:
        return f"Window in {self.location.name} is {self.status.name.lower()}."

    def __repr__(self) -> str:
        return f"Window(location={self.location!r}, status={self.status!r})"

    def toggle_status(self):
        """Example method to change window status, could cycle through statuses."""
        next_status = {
            WindowStatus.CLOSED: WindowStatus.TILTED,
            WindowStatus.TILTED: WindowStatus.OPEN,
            WindowStatus.OPEN: WindowStatus.CLOSED
        }
        self._status = next_status[self._status]
