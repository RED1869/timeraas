import logging
import os
import random
import requests

from flask import Flask, request, jsonify
from timeraas.manager import WindowManager
from timeraas.room import Room
from timeraas.window import Window, WindowStatus

app = Flask(__name__)

# Load environment variables for configuration
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
DEBUG_MODE = bool(int(os.getenv("DEBUG_MODE", "0")))

# Basic logger setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG if os.getenv("DEBUG_MODE") else logging.INFO)

# Console handler with color (optional)
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# File handler without ANSI color codes
file_handler = logging.FileHandler('timeraas.log', encoding='utf-8')
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# Initialize room and window manager
toilet = Room("toilet", 0)
toilet_window = Window(toilet)
toilet_window_manager = WindowManager(toilet_window)

if DISCORD_WEBHOOK_URL is None:
    logger.error("Discord webhook URL is not configured. No message will be sent out!")
if DEBUG_MODE:
    logger.debug("Debug mode is active")


def timer_expired():
    """Triggers actions when the timer expires if not in debug mode."""
    messages = [
        "Ich bin noch auf! 😱",
        "Mir wird kalt! 🥶",
        "Hier steigt gleich jemand ein! 🦹"
    ]
    if not DEBUG_MODE:
        send_discord_message(random.choice(messages))
    else:
        logger.debug("Would now have sent message to Discord.")


def send_discord_message(message):
    """Sends a message to the configured Discord webhook."""
    if not DISCORD_WEBHOOK_URL:
        logger.error("Discord webhook URL is not configured.")
        return

    data = {"content": message}
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        response.raise_for_status()
        logger.info("Message delivered successfully to Discord.")
    except requests.RequestException as e:
        logger.error(f"Failed to send message to Discord: {e}")


def validate_status(new_status):
    """Validates if the provided status is a recognized WindowStatus."""
    try:
        return WindowStatus[new_status]
    except KeyError:
        return None


@app.route('/home/toilet/window', methods=['POST'])
def update_window_status():
    try:
        new_status = request.json.get('status')
        validated_status = validate_status(new_status)
        if validated_status is None or validated_status not in {WindowStatus.OPEN, WindowStatus.CLOSED}:
            return jsonify({"error": 'Invalid status value. Must be "OPEN" or "CLOSED"'}), 400

        logger.info(f"Received request to update window status to {new_status}")

        if toilet_window_manager.status == WindowStatus.CLOSED and validated_status == WindowStatus.OPEN:
            duration = 600
            toilet_window_manager.start_timer(duration, timer_expired)
            logger.info(f"Timer started for {duration} seconds as window is now open.")
        elif toilet_window_manager.status == WindowStatus.OPEN and validated_status == WindowStatus.CLOSED:
            if toilet_window_manager.timer_expired:
                send_discord_message("Bin wieder zu, danke! 😊")
            toilet_window_manager.cancel_timer()
            logger.info("Timer cancelled as window is now closed.")

        toilet_window_manager.status = validated_status
        return jsonify({'status': toilet_window_manager.status.name}), 200

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        error_message = "An internal error occurred."
        if DEBUG_MODE:
            error_message += f" Details: {e}"
        return jsonify({"error": error_message}), 500


if __name__ == '__main__':
    logger.info("Starting the application...")
    app.run(host='0.0.0.0', port=5000, debug=DEBUG_MODE)
    logger.info("Application shutdown.")
