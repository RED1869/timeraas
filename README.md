# Timeraas - Smart Window Monitoring with Fritz!DECT 350

### Description  
Timeraas is a smart window monitoring and alert system built to work seamlessly with the AVM Fritz!DECT 350 magnetic door/window sensors. Designed for integration with smart home setups, Timeraas monitors window states (open, closed, tilted) and sends timely alerts if windows are left open for too long, ensuring energy efficiency and enhanced security. Using a Flask-based API and real-time notifications through Discord, the system provides a straightforward way to stay informed about window statuses in your home or office.

### Key Features
- **Fritz!DECT 350 Integration**: Automatically detects window state changes using AVM Fritz!DECT 350 sensors and responds accordingly.
- **Automated Alerts**: Triggers notifications to Discord if a window is left open beyond a configurable period.
- **Configurable and Scalable**: Allows easy setup and monitoring for multiple windows, with adjustable timer settings and debug modes.
- **Flexible API Endpoint**: Provides a REST API to interact with the system, making it easy to integrate with other smart home controls.

### Technical Stack
- **Framework**: Flask (Python)
- **Notifications**: Discord Webhook
- **Dependencies**: AVM Fritz!DECT 350 sensors, Discord integration, environment-based configuration.

### Quick Start
1. Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

2. Set environment variable DISCORD_WEBHOOK_URL.

3. Run the application:
  ```bash
  python -m timeraas.app
  ```
