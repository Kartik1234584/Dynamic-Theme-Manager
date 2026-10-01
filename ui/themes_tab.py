from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QScrollArea, QLabel, 
                             QPushButton, QMessageBox, QInputDialog)
from PyQt6.QtCore import Qt
from ui.components.image_card import ImageCard
from ui.components.flow_layout import FlowLayout
import random

class ThemesTab(QWidget):
    def __init__(self, app_core):
        super().__init__()
        self.core = app_core
        self.setup_ui()
        self.load_categories()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header Row
        header_layout = QHBoxLayout()
        header = QLabel("Themes Collection")
        header.setObjectName("title")
        header_layout.addWidget(header)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        subtitle = QLabel("Select an active theme to rotate wallpapers from. Microsoft Store themes are automatically synced here.")
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)
        
        # Scroll Area for themes
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        self.grid_widget = QWidget()
        self.grid_widget.setStyleSheet("background-color: transparent;")
        self.grid_layout = FlowLayout(self.grid_widget, margin=0, hSpacing=25, vSpacing=25)
        
        self.scroll.setWidget(self.grid_widget)
        layout.addWidget(self.scroll)
        
        self.setLayout(layout)
        
    def load_categories(self):
        # Clear layout
        for i in reversed(range(self.grid_layout.count())): 
            self.grid_layout.itemAt(i).widget().setParent(None)
            
        categories = self.core.db.get_all_categories()
        
        for c in categories:
            cat_id, cat_name, source = c['id'], c['name'], c.get('source', 'Custom')
            if cat_name.lower() == "random" or source == "Custom":
                continue
                
            wallpapers = self.core.db.get_wallpapers_by_category(cat_name)
            count = len(wallpapers)
            
            preview_path = ""
            if wallpapers:
                preview_path = random.choice(wallpapers)['path']
                
            card = ImageCard(preview_path, cat_name, f"{count} Wallpapers", source)
            card.setCursor(Qt.CursorShape.PointingHandCursor)
            card.mousePressEvent = lambda event, name=cat_name: self.set_active_theme(name)
            
            self.grid_layout.addWidget(card)
                
    def set_active_theme(self, theme_name):
        self.core.settings.set("last_theme", theme_name)
        self.core.apply_settings()
        
        # Instantly trigger wallpaper rotation to provide premium feedback
        self.core.force_next_wallpaper()
