import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from core.database_manager import DatabaseManager
from core.settings_manager import SettingsManager
from core.wallpaper_manager import WallpaperManager
from core.timer_manager import TimerManager
from core.theme_scanner import WindowsThemeScanner
from core.scheduler_manager import SchedulerManager
from ui.main_window import MainWindow

import traceback
from datetime import datetime

def global_exception_handler(exctype, value, tb):
    """Log any unhandled exceptions to crash.log before exiting."""
    error_msg = f"Crash at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    error_msg += "".join(traceback.format_exception(exctype, value, tb))
    error_msg += "\n" + "="*40 + "\n"
    
    try:
        with open("crash.log", "a") as f:
            f.write(error_msg)
    except Exception:
        pass
        
    sys.__excepthook__(exctype, value, tb)

sys.excepthook = global_exception_handler

try:
    import pyi_splash
except ImportError:
    pyi_splash = None
class AppCore:
    """Core application controller that bridges UI and managers."""
    def __init__(self):
        self.db = DatabaseManager()
        self.settings = SettingsManager(self.db)
        self.wallpaper_manager = WallpaperManager(self.db)
        self.theme_scanner = WindowsThemeScanner(self.db)
        self.scheduler_manager = SchedulerManager()
        self.timer_manager = TimerManager()
        
        self.timer_manager.timeout.connect(self.on_timer_tick)
        
        self.apply_settings()
        
        # We can't show toast easily from core unless we pass a reference to MainWindow
        # We'll let MainWindow handle the connection if we want toasts.
        # But let's run the initial scan.
        self.theme_scanner.scan_initial_themes()
        
    def apply_settings(self):
        """Applies settings from the SettingsManager."""
        interval = self.settings.get("timer_interval")
        self.timer_manager.set_interval(interval)
        
    def toggle_timer(self):
        if self.timer_manager.is_running:
            self.timer_manager.stop()
        else:
            self.timer_manager.start()
            
    def on_timer_tick(self):
        self.force_next_wallpaper()
        
    def force_next_wallpaper(self):
        theme = self.scheduler_manager.get_current_scheduled_theme()
        if not theme:
            theme = self.settings.get("last_theme")
            
        random_mode = self.settings.get("random_mode")
        self.wallpaper_manager.change_wallpaper(theme, random_mode)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Dynamic Theme Manager")
    
    # Set the application icon for the window title bar and taskbar
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_path, "icon.png")
    
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # Optional: Set global stylesheet here or let main window do it.
    
    # Initialize Core System
    core = AppCore()
    
    # Initialize Main Window
    window = MainWindow(core)
    
    # Optional: startup behavior
    # If starting on boot, might want to start hidden. For now, show normally.
    window.show()
    
    # Start timer automatically if preferred (we'll start it)
    core.timer_manager.start()
    
    # Close pyinstaller splash screen if it exists
    if pyi_splash:
        pyi_splash.close()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
