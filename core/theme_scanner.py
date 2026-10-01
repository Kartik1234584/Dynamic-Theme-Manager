import os
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from PyQt6.QtCore import QFileSystemWatcher

class WindowsThemeScanner(QObject):
    """Scans and monitors the Windows Themes directory for imported themes."""
    
    theme_imported = pyqtSignal(str, int) # theme_name, wallpaper_count
    
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.themes_dir = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'Windows', 'Themes')
        self.watcher = QFileSystemWatcher()
        self.debounce_timer = QTimer()
        self.debounce_timer.setSingleShot(True)
        self.debounce_timer.timeout.connect(self.scan_initial_themes)
        
        if os.path.exists(self.themes_dir):
            self.watcher.addPath(self.themes_dir)
            self.watcher.directoryChanged.connect(self.on_directory_changed)
            
    def scan_initial_themes(self):
        """Scans the windows themes directory on startup."""
        if not os.path.exists(self.themes_dir):
            return 0
            
        imported_count = 0
        for item in os.listdir(self.themes_dir):
            theme_path = os.path.join(self.themes_dir, item)
            if os.path.isdir(theme_path):
                # A Microsoft Store theme usually has a DesktopBackground folder
                bg_path = os.path.join(theme_path, 'DesktopBackground')
                if os.path.exists(bg_path):
                    count = self.import_theme(item, bg_path)
                    if count > 0:
                        imported_count += 1
        return imported_count
        
    def on_directory_changed(self, path):
        """Triggered when the Windows Theme folder changes."""
        # Proper debounce: wait 5 seconds after the LAST file change before scanning
        # This prevents spamming notifications while Windows is extracting 50+ images
        self.debounce_timer.start(5000)
        
    def import_theme(self, theme_name, bg_path):
        """Imports wallpapers from a detected Windows theme folder."""
        # Clean up theme name
        clean_name = theme_name.replace('_', ' ').title()
        
        # Check if theme exists in DB, if not create as Windows source
        # We will add an add_theme method to DB manager
        theme_id = self.db.add_theme(clean_name, source='Windows')
        if not theme_id:
            theme_id = self.db.get_category_id(clean_name)
            
        if not theme_id:
            return 0
            
        added_wallpapers = 0
        supported = ('.jpg', '.jpeg', '.png', '.webp')
        
        for file in os.listdir(bg_path):
            if file.lower().endswith(supported):
                file_path = os.path.join(bg_path, file)
                res = self.db.add_wallpaper(file_path, file, clean_name)
                if res is not None:
                    added_wallpapers += 1
                    
        if added_wallpapers > 0:
            self.theme_imported.emit(clean_name, added_wallpapers)
            
        return added_wallpapers
