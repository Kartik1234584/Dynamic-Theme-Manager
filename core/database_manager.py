import sqlite3
import os

class DatabaseManager:
    """Manages the SQLite database for the Dynamic Theme Manager."""
    
    def __init__(self):
        self.db_path = os.path.join("database", "wallpapers.db")
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_db()

    def _get_connection(self):
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            
            # Enable foreign keys for SQLite
            conn.execute("PRAGMA foreign_keys = ON")
            return conn
        except sqlite3.Error as e:
            print(f"Error connecting to SQLite: {e}")
            return None

    def init_db(self):
        conn = self._get_connection()
        if not conn:
            return
            
        cursor = conn.cursor()
        
        # 1. Themes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS themes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                theme_name VARCHAR(255) UNIQUE,
                accent_color VARCHAR(50) DEFAULT '#0078D4',
                source VARCHAR(50) DEFAULT 'Custom',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert default themes
        default_themes = ["Nature", "Dark", "Anime", "Minimal", "Cars", "Random"]
        for t in default_themes:
            cursor.execute("INSERT OR IGNORE INTO themes (theme_name) VALUES (?)", (t,))
            
        # 2. Wallpapers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wallpapers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_name VARCHAR(255),
                file_path TEXT,
                resolution VARCHAR(50) DEFAULT 'Unknown',
                category_id INTEGER,
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES themes(id) ON DELETE SET NULL
            )
        ''')
        
        # 3. Settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timer_interval INTEGER DEFAULT 300,
                shuffle_enabled BOOLEAN DEFAULT 1,
                startup_enabled BOOLEAN DEFAULT 0,
                dark_mode BOOLEAN DEFAULT 1,
                last_selected_theme VARCHAR(255) DEFAULT 'Random'
            )
        ''')
        
        # Initialize settings row if empty
        cursor.execute("SELECT COUNT(*) FROM settings")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO settings (id) VALUES (1)")
        
        # 4. History table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                wallpaper_id INTEGER,
                changed_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (wallpaper_id) REFERENCES wallpapers(id) ON DELETE CASCADE
            )
        ''')
        
        # 5. Favorites table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                wallpaper_id INTEGER UNIQUE,
                added_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (wallpaper_id) REFERENCES wallpapers(id) ON DELETE CASCADE
            )
        ''')
        
        conn.commit()
        cursor.close()
        conn.close()

    def execute_query(self, query, params=(), fetch_one=False, fetch_all=False):
        conn = self._get_connection()
        if not conn:
            if fetch_all: return []
            if fetch_one: return {}
            return None
            
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            if fetch_one:
                row = cursor.fetchone()
                result = dict(row) if row else {}
            elif fetch_all:
                rows = cursor.fetchall()
                result = [dict(row) for row in rows]
            else:
                conn.commit()
                result = cursor.lastrowid
            return result
        except sqlite3.Error as e:
            print(f"Database error executing {query}: {e}")
            if fetch_all: return []
            if fetch_one: return {}
            return None
        finally:
            cursor.close()
            conn.close()

    # --- Themes Methods ---
    def add_theme(self, name, source='Custom'):
        # Attempt to migrate schema if source column is missing
        try:
            self.execute_query("ALTER TABLE themes ADD COLUMN source VARCHAR(50) DEFAULT 'Custom'")
        except Exception:
            pass # column likely exists
            
        exists = self.get_category_id(name)
        if exists:
            return exists
            
        return self.execute_query("INSERT INTO themes (theme_name, source) VALUES (?, ?)", (name, source))
        
    def get_all_categories(self):
        try:
            self.execute_query("ALTER TABLE themes ADD COLUMN source VARCHAR(50) DEFAULT 'Custom'")
        except Exception:
            pass
        return self.execute_query("SELECT id, theme_name as name, source FROM themes", fetch_all=True)

    def get_category_id(self, name):
        result = self.execute_query("SELECT id FROM themes WHERE theme_name = ?", (name,), fetch_one=True)
        return result['id'] if result else None

    # --- Wallpapers Methods ---
    def add_wallpaper(self, path, filename, category_name="Random"):
        cat_id = self.get_category_id(category_name)
        if not cat_id:
            cat_id = self.get_category_id("Random")
            
        exists = self.execute_query("SELECT id FROM wallpapers WHERE file_path = ?", (path,), fetch_one=True)
        if exists:
            return None
            
        return self.execute_query('''
            INSERT INTO wallpapers (file_path, file_name, category_id)
            VALUES (?, ?, ?)
        ''', (path, filename, cat_id))
        
    def get_wallpapers_by_category(self, category_name):
        cat_id = self.get_category_id(category_name)
        if cat_id:
            return self.execute_query("SELECT id, file_path as path, file_name as filename FROM wallpapers WHERE category_id = ?", (cat_id,), fetch_all=True)
        return []

    def get_all_wallpapers(self):
        return self.execute_query("SELECT id, file_path as path, file_name as filename, category_id FROM wallpapers", fetch_all=True)
        
    def count_wallpapers(self):
        result = self.execute_query("SELECT COUNT(*) as count FROM wallpapers", fetch_one=True)
        return result['count'] if result else 0

    def update_wallpaper_category(self, wallpaper_id, category_id):
        return self.execute_query("UPDATE wallpapers SET category_id = ? WHERE id = ?", (category_id, wallpaper_id))
        
    def remove_wallpaper_by_path(self, path):
        self.execute_query("DELETE FROM wallpapers WHERE file_path LIKE ?", (f"{path}%",))
        return True

    # --- Settings Methods ---
    def get_settings(self):
        return self.execute_query("SELECT * FROM settings WHERE id = 1", fetch_one=True)
        
    def update_setting(self, key, value):
        column_map = {
            "timer_interval": "timer_interval",
            "start_on_startup": "startup_enabled",
            "last_theme": "last_selected_theme",
            "random_mode": "shuffle_enabled",
            "dark_mode": "dark_mode"
        }
        db_col = column_map.get(key, key)
        self.execute_query(f"UPDATE settings SET {db_col} = ? WHERE id = 1", (value,))

    # --- History & Favorites Methods ---
    def add_history(self, path):
        w = self.execute_query("SELECT id FROM wallpapers WHERE file_path = ?", (path,), fetch_one=True)
        if w and 'id' in w:
            self.execute_query("DELETE FROM history WHERE wallpaper_id = ?", (w['id'],))
            self.execute_query("INSERT INTO history (wallpaper_id) VALUES (?)", (w['id'],))

    def get_history(self, limit=50):
        return self.execute_query('''
            SELECT h.changed_time, w.file_path, w.file_name, t.theme_name
            FROM history h
            JOIN wallpapers w ON h.wallpaper_id = w.id
            LEFT JOIN themes t ON w.category_id = t.id
            ORDER BY h.changed_time DESC LIMIT ?
        ''', (limit,), fetch_all=True)
        
    def add_favorite(self, path):
        w = self.execute_query("SELECT id FROM wallpapers WHERE file_path = ?", (path,), fetch_one=True)
        if w and 'id' in w:
            self.execute_query("INSERT OR IGNORE INTO favorites (wallpaper_id) VALUES (?)", (w['id'],))

    def remove_favorite(self, path):
        w = self.execute_query("SELECT id FROM wallpapers WHERE file_path = ?", (path,), fetch_one=True)
        if w and 'id' in w:
            self.execute_query("DELETE FROM favorites WHERE wallpaper_id = ?", (w['id'],))

    def get_favorites(self):
        return self.execute_query('''
            SELECT w.file_path as path, w.file_name as filename, t.theme_name as category
            FROM favorites f
            JOIN wallpapers w ON f.wallpaper_id = w.id
            LEFT JOIN themes t ON w.category_id = t.id
            ORDER BY f.added_time DESC
        ''', fetch_all=True)

    def is_favorite(self, path):
        w = self.execute_query("SELECT id FROM wallpapers WHERE file_path = ?", (path,), fetch_one=True)
        if w and 'id' in w:
            fav = self.execute_query("SELECT id FROM favorites WHERE wallpaper_id = ?", (w['id'],), fetch_one=True)
            return bool(fav)
        return False
