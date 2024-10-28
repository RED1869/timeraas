import requests
import unittest

from unittest.mock import patch, Mock
from timeraas.app import app, toilet_window_manager, DISCORD_WEBHOOK_URL, timer_expired, send_discord_message

class TestApp(unittest.TestCase):

    def setUp(self):
        """Set up a Flask test client and ensure each test starts with a closed window."""
        self.client = app.test_client()
        toilet_window_manager.status = toilet_window_manager.window.status = 'CLOSED'

    @patch('timeraas.app.requests.post')
    def test_update_window_status_open(self, mock_post):
        """Test opening the window and starting the timer."""
        response = self.client.post('/home/toilet/window', json={'status': 'OPEN'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'OPEN')
        self.assertTrue(toilet_window_manager._timer is not None)  # Timer should be set
        toilet_window_manager.cancel_timer()  # Timer should not be running anymore

    @patch('timeraas.app.requests.post')
    def test_update_window_status_close(self, mock_post):
        """Test closing the window and cancelling the timer."""
        # First, open the window to start the timer
        self.client.post('/home/toilet/window', json={'status': 'OPEN'})

        # Now, close the window
        response = self.client.post('/home/toilet/window', json={'status': 'CLOSED'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'CLOSED')
        self.assertTrue(toilet_window_manager._timer is None)  # Timer should be cancelled

    def test_invalid_status(self):
        """Test sending an invalid status to the window endpoint."""
        response = self.client.post('/home/toilet/window', json={'status': 'INVALID'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], 'Invalid status value. Must be "OPEN" or "CLOSED"')

    @patch('timeraas.app.requests.post')
    def test_send_discord_message_success(self, mock_post):
        """Test successful sending of a message to Discord."""
        mock_post.return_value.status_code = 204

        # Ensure DISCORD_WEBHOOK_URL is set for this test
        with patch('timeraas.app.DISCORD_WEBHOOK_URL', 'http://mock.url'):
            send_discord_message("Test message")

        # Assert that post was called with the correct arguments
        mock_post.assert_called_once_with('http://mock.url', json={"content": "Test message"})

    @patch('timeraas.app.requests.post')
    @patch('timeraas.app.logger')
    def test_send_discord_message_failure(self, mock_logger, mock_post):
        """Test failure when sending a message to Discord."""
        mock_post.side_effect = requests.RequestException("Network error")

        # Ensure DISCORD_WEBHOOK_URL is set for this test
        with patch('timeraas.app.DISCORD_WEBHOOK_URL', 'http://mock.url'):
            send_discord_message("Test message")

        # Assert that the error log was called with the expected message
        mock_logger.error.assert_called_once()
        self.assertIn("Failed to send message to Discord", mock_logger.error.call_args[0][0])

    @patch('timeraas.app.send_discord_message')
    def test_timer_expired(self, mock_send_message):
        """Test that timer expiration triggers a message to Discord."""
        timer_expired()  # Simulate timer expiration
        mock_send_message.assert_called_once()  # Message should be sent to Discord

    def test_timer_expired_debug_mode(self):
        """Test that in DEBUG_MODE, no message is sent on timer expiration."""
        with patch('timeraas.app.DEBUG_MODE', True), patch('timeraas.app.send_discord_message') as mock_send_message:
            timer_expired()
            mock_send_message.assert_not_called()  # No message should be sent

    def test_update_window_status_internal_error(self):
        """Test that an internal error is handled correctly and returns a 500 response."""
        with patch('timeraas.app.validate_status', side_effect=Exception("Test error")):
            response = self.client.post('/home/toilet/window', json={'status': 'OPEN'})
            self.assertEqual(response.status_code, 500)
            self.assertIn("An internal error occurred", response.json['error'])


if __name__ == '__main__':
    unittest.main()
