import threading

from timeraas.window import Window


class WindowManager:
    def __init__(self, window: Window):
        self._window = window
        self._timer = None
        self._timer_expired = False
        self._lock = threading.Lock()  # Lock for thread safety

    @property
    def window(self) -> Window:
        """Read-only access to the associated Window."""
        return self._window

    def _on_timer_expire(self, callback):
        """Handles the timer expiration event and executes the callback."""
        with self._lock:
            self._timer_expired = True
            if callback and callable(callback):
                callback()
            self._timer = None

    def start_timer(self, duration: int, callback=None):
        """Starts a timer for the specified duration in seconds with an optional callback."""
        if not isinstance(duration, int) or duration <= 0:
            raise ValueError("Duration must be a positive integer.")
        if callback and not callable(callback):
            raise ValueError("Callback must be a callable function.")

        with self._lock:
            if self._timer is not None:
                self._timer.cancel()
            self._timer_expired = False
            self._timer = threading.Timer(duration, self._on_timer_expire, [callback])
            self._timer.start()

    def cancel_timer(self):
        """Cancels the active timer, if any, and resets timer expiration status."""
        with self._lock:
            if self._timer is not None:
                self._timer.cancel()
                self._timer = None
            self._timer_expired = False

    @property
    def status(self):
        return self._window.status

    @status.setter
    def status(self, status):
        self._window.status = status

    @property
    def timer_expired(self) -> bool:
        """Indicates if the timer has expired."""
        with self._lock:
            return self._timer_expired

    def __str__(self) -> str:
        timer_status = "expired" if self._timer_expired else "active" if self._timer else "inactive"
        return f"WindowManager for {self.window} with timer {timer_status}."

    def __repr__(self) -> str:
        return f"WindowManager(window={self.window!r}, timer_expired={self._timer_expired})"
