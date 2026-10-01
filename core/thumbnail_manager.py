import os
from PIL import Image
import hashlib
from PyQt6.QtCore import QThread, pyqtSignal

class ThumbnailGeneratorThread(QThread):
    """Background thread to generate a thumbnail if it doesn't exist."""
    finished = pyqtSignal(str, str, int) # original_path, thumb_path, db_id
    
    def __init__(self, original_path, db_id, cache_dir="cache/thumbnails"):
        super().__init__()
        self.original_path = original_path
        self.db_id = db_id
        self.cache_dir = cache_dir
        
    def run(self):
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir, exist_ok=True)
            
        # Create a unique filename for the thumbnail based on the absolute path
        path_hash = hashlib.md5(self.original_path.encode('utf-8')).hexdigest()
        thumb_name = f"{path_hash}.jpg"
        thumb_path = os.path.join(self.cache_dir, thumb_name)
        
        if not os.path.exists(thumb_path) and os.path.exists(self.original_path):
            try:
                # Open original image and generate a thumbnail
                with Image.open(self.original_path) as img:
                    # Convert to RGB if necessary (e.g. RGBA pngs)
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    # Use 'contain' mode essentially by setting a max size
                    img.thumbnail((600, 400), Image.Resampling.LANCZOS)
                    img.save(thumb_path, "JPEG", quality=85)
            except Exception as e:
                print(f"Failed to generate thumbnail for {self.original_path}: {e}")
                self.finished.emit(self.original_path, "", self.db_id)
                return
                
        self.finished.emit(self.original_path, thumb_path, self.db_id)
