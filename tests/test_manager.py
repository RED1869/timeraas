import unittest
from unittest.mock import patch, Mock
from timeraas.room import Room
from timeraas.window import Window, WindowStatus
from timeraas.manager import WindowManager
import threading


class TestWindowManager(unittest.TestCase):

    def setUp(self):
        """Set up a Room, Window, and WindowManager instance for testing."""
        self.room = Room(name="Living Room", floor=1)
        self.window = Window(self.room)
        self.manager = WindowManager(self.window)

    @patch('threading.Timer')
    def test_start_timer(self, mock_timer):
        """Test starting a timer sets up a timer correctly."""
        callback = Mock()
        self.manager.start_timer(600, callback)
        mock_timer.assert_called_once_with(600, self.manager._on_timer_expire, [callback])
        self.assertIsNotNone(self.manager._timer)

    def test_cancel_timer(self):
        """Test cancelling an active timer."""
        with patch.object(threading.Timer, 'cancel', return_value=None) as mock_cancel:
            callback = Mock()
            self.manager.start_timer(600, callback)
            self.manager.cancel_timer()
            mock_cancel.assert_called_once()
            self.assertIsNone(self.manager._timer)
            self.assertFalse(self.manager._timer_expired)

    def test_status_property(self):
        """Test that status property updates window status correctly."""
        self.assertEqual(self.manager.status, WindowStatus.CLOSED)
        self.manager.status = WindowStatus.OPEN
        self.assertEqual(self.window.status, WindowStatus.OPEN)
        self.assertEqual(self.manager.status, WindowStatus.OPEN)

    def test_timer_expired_property(self):
        """Test the timer_expired property reflects the correct timer status."""
        self.assertFalse(self.manager.timer_expired)
        self.manager._timer_expired = True
        self.assertTrue(self.manager.timer_expired)

    @patch('threading.Timer')
    def test_on_timer_expire(self, mock_timer):
        """Test that the timer expiration function sets timer_expired to True."""
        callback = Mock()
        # Simulate expiration by manually calling _on_timer_expire
        self.manager._on_timer_expire(callback)

        # Check that timer_expired is True and callback is called
        self.assertTrue(self.manager.timer_expired)
        callback.assert_called_once()

    def test_timer_expired_callback_called(self):
        """Test that the expiration callback is called when the timer expires."""
        callback = Mock()
        self.manager._on_timer_expire(callback)
        callback.assert_called_once()
        self.assertTrue(self.manager.timer_expired)

    @patch('threading.Timer')
    def test_timer_already_running(self, mock_timer):
        """Test that starting a new timer cancels an existing timer."""
        callback1 = Mock()
        callback2 = Mock()
        self.manager.start_timer(600, callback1)
        mock_timer_instance = mock_timer.return_value
        mock_timer_instance.cancel = Mock()

        self.manager.start_timer(300, callback2)
        mock_timer_instance.cancel.assert_called_once()
        mock_timer.assert_called_with(300, self.manager._on_timer_expire, [callback2])

    def test_str_representation(self):
        """Test the __str__ representation of WindowManager."""
        expected_status = "inactive"
        self.assertEqual(str(self.manager), f"WindowManager for {self.window} with timer {expected_status}.")
        self.manager.start_timer(600, Mock())
        expected_status = "active"
        self.assertEqual(str(self.manager), f"WindowManager for {self.window} with timer {expected_status}.")

    def test_repr_representation(self):
        """Test the __repr__ representation of WindowManager."""
        self.assertEqual(repr(self.manager), f"WindowManager(window={self.window!r}, timer_expired=False)")


if __name__ == "__main__":
    unittest.main()
