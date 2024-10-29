import unittest

from timeraas.room import Room


class TestRoom(unittest.TestCase):

    def test_initialization(self):
        """Test that a Room initializes with correct name and floor."""
        room = Room(name="Living Room", floor=2)
        self.assertEqual(room.name, "Living Room")
        self.assertEqual(room.floor, 2)

    def test_invalid_name(self):
        """Test that setting an invalid name raises ValueError."""
        with self.assertRaises(ValueError) as context:
            Room(name="", floor=1)
        self.assertEqual(str(context.exception), "Room name must be a non-empty string.")

        with self.assertRaises(ValueError) as context:
            Room(name="   ", floor=1)
        self.assertEqual(str(context.exception), "Room name must be a non-empty string.")

    def test_invalid_floor(self):
        """Test that setting a non-integer floor raises ValueError."""
        with self.assertRaises(ValueError) as context:
            Room(name="Kitchen", floor="Second")
        self.assertEqual(str(context.exception), "Floor must be an integer.")

        with self.assertRaises(ValueError) as context:
            Room(name="Kitchen", floor=1.5)
        self.assertEqual(str(context.exception), "Floor must be an integer.")

    def test_set_name(self):
        """Test setting a valid name after initialization."""
        room = Room(name="Office", floor=1)
        room.name = "Study"
        self.assertEqual(room.name, "Study")

    def test_set_floor(self):
        """Test setting a valid floor after initialization."""
        room = Room(name="Office", floor=1)
        room.floor = 3
        self.assertEqual(room.floor, 3)

    def test_str_representation(self):
        """Test the __str__ representation of Room."""
        room = Room(name="Living Room", floor=2)
        self.assertEqual(str(room), "Room(name='Living Room', floor=2)")

    def test_repr_representation(self):
        """Test the __repr__ representation of Room."""
        room = Room(name="Living Room", floor=2)
        self.assertEqual(repr(room), "Room(name='Living Room', floor=2)")

    def test_equality(self):
        """Test that two Room instances with the same name and floor are equal."""
        room1 = Room(name="Kitchen", floor=1)
        room2 = Room(name="Kitchen", floor=1)
        room3 = Room(name="Bathroom", floor=1)
        self.assertEqual(room1, room2)
        self.assertNotEqual(room1, room3)

    def test_hash(self):
        """Test that Room instances with the same name and floor have the same hash."""
        room1 = Room(name="Bedroom", floor=1)
        room2 = Room(name="Bedroom", floor=1)
        room3 = Room(name="Guest Room", floor=1)
        self.assertEqual(hash(room1), hash(room2))
        self.assertNotEqual(hash(room1), hash(room3))


if __name__ == "__main__":
    unittest.main()
