import json
import os
from datetime import datetime

class SchedulerManager:
    def __init__(self):
        self.file_path = os.path.join("settings", "scheduler.json")
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        self.settings = self.load_settings()

    def load_settings(self):
        default = {
            "enabled": False,
            "morning": "Nature",
            "afternoon": "Cars",
            "evening": "Minimal",
            "night": "Dark"
        }
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as f:
                    data = json.load(f)
                default.update(data)
            except Exception:
                pass
        return default

    def save_settings(self, settings):
        self.settings = settings
        try:
            with open(self.file_path, "w") as f:
                json.dump(self.settings, f, indent=4)
        except Exception:
            pass

    def get_current_scheduled_theme(self):
        if not self.settings.get("enabled"):
            return None
            
        hour = datetime.now().hour
        if 6 <= hour < 12:
            return self.settings.get("morning", "Random")
        elif 12 <= hour < 18:
            return self.settings.get("afternoon", "Random")
        elif 18 <= hour < 22:
            return self.settings.get("evening", "Random")
        else:
            return self.settings.get("night", "Random")
