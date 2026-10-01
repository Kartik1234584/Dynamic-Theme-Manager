class SettingsManager:
    """Manages application settings using the MySQL database."""
    
    def __init__(self, db_manager):
        self.db = db_manager
        self.default_settings = {
            "timer_interval": 300,
            "start_on_startup": False,
            "last_theme": "Random",
            "random_mode": True,
            "dark_mode": True
        }
        
    def load_settings(self):
        db_settings = self.db.get_settings()
        if db_settings:
            return {
                "timer_interval": db_settings.get("timer_interval", 300),
                "start_on_startup": bool(db_settings.get("startup_enabled", False)),
                "last_theme": db_settings.get("last_selected_theme", "Random"),
                "random_mode": bool(db_settings.get("shuffle_enabled", True)),
                "dark_mode": bool(db_settings.get("dark_mode", True))
            }
        return self.default_settings.copy()
            
    def get(self, key):
        settings = self.load_settings()
        return settings.get(key, self.default_settings.get(key))
        
    def set(self, key, value):
        self.db.update_setting(key, value)
