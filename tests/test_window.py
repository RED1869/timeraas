import unittest

from timeraas.room import Room
from timeraas.window import Window, WindowStatus


class TestWindow(unittest.TestCase):

    def setUp(self):
        """Set up a Room and Window instance for testing."""
        self.room = Room("Living Room", 1)
        self.window = Window(self.room)

    def test_initial_status(self):
        """Test that the window initializes with CLOSED status."""
        self.assertEqual(self.window.status, WindowStatus.CLOSED)

    def test_set_status_enum(self):
        """Test setting status using WindowStatus enum values."""
        self.window.status = WindowStatus.OPEN
        self.assertEqual(self.window.status, WindowStatus.OPEN)

        self.window.status = WindowStatus.TILTED
        self.assertEqual(self.window.status, WindowStatus.TILTED)

    def test_set_status_string(self):
        """Test setting status using string names, case-insensitive."""
        self.window.status = "open"
        self.assertEqual(self.window.status, WindowStatus.OPEN)

        self.window.status = "CLOSED"
        self.assertEqual(self.window.status, WindowStatus.CLOSED)

    def test_invalid_status_string(self):
        """Test that setting an invalid status string raises a ValueError."""
        with self.assertRaises(ValueError) as context:
            self.window.status = "INVALID"
        self.assertEqual(str(context.exception), "INVALID is not a valid WindowStatus.")

    def test_invalid_status_type(self):
        """Test that setting an invalid status type raises a TypeError."""
        with self.assertRaises(TypeError) as context:
            self.window.status = 123
        self.assertEqual(str(context.exception), "Status must be a WindowStatus enum or valid status name as string.")

    def test_toggle_status(self):
        """Test the toggle_status method cycles through CLOSED -> TILTED -> OPEN -> CLOSED."""
        self.assertEqual(self.window.status, WindowStatus.CLOSED)

        self.window.toggle_status()
        self.assertEqual(self.window.status, WindowStatus.TILTED)

        self.window.toggle_status()
        self.assertEqual(self.window.status, WindowStatus.OPEN)

        self.window.toggle_status()
        self.assertEqual(self.window.status, WindowStatus.CLOSED)

    def test_location_is_read_only(self):
        """Test that the location property is read-only."""
        with self.assertRaises(AttributeError):
            # noinspection PyPropertyAccess
            self.window.location = Room("Kitchen", 1)

    def test_str_representation(self):
        """Test the string representation of the Window instance."""
        self.assertEqual(str(self.window), "Window in Living Room is closed.")
        self.window.status = WindowStatus.OPEN
        self.assertEqual(str(self.window), "Window in Living Room is open.")

    def test_repr_representation(self):
        """Test the repr representation of the Window instance."""
        self.assertEqual(repr(self.window), f"Window(location={self.room!r}, status={WindowStatus.CLOSED!r})")


if __name__ == "__main__":
    unittest.main()
