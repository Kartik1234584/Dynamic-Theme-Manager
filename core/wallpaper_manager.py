import os
import random
from PyQt6.QtCore import QObject, pyqtSignal
from core.database_manager import DatabaseManager
from utils.windows_api import set_wallpaper

class WallpaperManager(QObject):
    """Manages wallpaper folders, scanning, and current wallpaper state."""
    
    wallpaper_changed = pyqtSignal(str) # Emits the new wallpaper path
    
    def __init__(self, db_manager: DatabaseManager):
        super().__init__()
        self.db = db_manager
        self.supported_extensions = ('.jpg', '.jpeg', '.png', '.webp')
        self.current_wallpaper = None
        self.history = []

    def scan_folder(self, folder_path):
        """Scans a folder for supported images and adds them to DB."""
        if not os.path.exists(folder_path):
            return 0
            
        added_count = 0
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(self.supported_extensions):
                    file_path = os.path.join(root, file)
                    file_path = os.path.normpath(file_path)
                    res = self.db.add_wallpaper(file_path, file)
                    if res is not None:
                        added_count += 1
        return added_count

    def add_folder(self, path):
        """Scans folder and adds wallpapers."""
        path = os.path.normpath(path)
        return self.scan_folder(path)

    def remove_folder(self, path):
        """Removes a folder's wallpapers from DB."""
        path = os.path.normpath(path)
        return self.db.remove_wallpaper_by_path(path)

    def get_next_wallpaper(self, theme_name="Random", random_mode=True):
        """Retrieves the next wallpaper based on theme and mode."""
        if theme_name == "Random":
            wallpapers = self.db.get_all_wallpapers()
        else:
            wallpapers = self.db.get_wallpapers_by_category(theme_name)
            
        if not wallpapers:
            return None

        # Filter out history to avoid repeating (if possible)
        available = [w for w in wallpapers if w['path'] not in self.history[-3:]]
        if not available:
            available = wallpapers # fallback if all recent
            
        if random_mode:
            selected = random.choice(available)
        else:
            if self.current_wallpaper:
                try:
                    idx = next(i for i, w in enumerate(wallpapers) if w['path'] == self.current_wallpaper)
                    selected = wallpapers[(idx + 1) % len(wallpapers)]
                except StopIteration:
                    selected = available[0]
            else:
                selected = available[0]
                
        return selected['path']

    def change_wallpaper(self, theme_name="Random", random_mode=True):
        """Changes the desktop wallpaper."""
        path = self.get_next_wallpaper(theme_name, random_mode)
        if path and os.path.exists(path):
            if set_wallpaper(path):
                self.current_wallpaper = path
                self.history.append(path)
                self.db.add_history(path)
                if len(self.history) > 10:
                    self.history.pop(0)
                self.wallpaper_changed.emit(path)
                return True
        return False
        
    def set_specific_wallpaper(self, path):
        if path and os.path.exists(path):
            if set_wallpaper(path):
                self.current_wallpaper = path
                self.history.append(path)
                self.db.add_history(path)
                if len(self.history) > 10:
                    self.history.pop(0)
                self.wallpaper_changed.emit(path)
                return True
        return False
