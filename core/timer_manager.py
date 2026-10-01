from PyQt6.QtCore import QObject, QTimer, pyqtSignal

class TimerManager(QObject):
    """Manages the automatic wallpaper rotation timer."""
    
    timeout = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self._on_timeout)
        self.is_running = False
        
    def set_interval(self, seconds):
        """Sets the timer interval in seconds."""
        # QTimer uses milliseconds
        was_running = self.is_running
        self.timer.setInterval(int(seconds * 1000))
        if was_running:
            self.start()

    def start(self):
        """Starts the timer."""
        if self.timer.interval() > 0:
            self.timer.start()
            self.is_running = True

    def stop(self):
        """Stops the timer."""
        self.timer.stop()
        self.is_running = False
        
    def _on_timeout(self):
        self.timeout.emit()
