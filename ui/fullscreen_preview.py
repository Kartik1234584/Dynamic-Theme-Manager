from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QKeySequence, QShortcut
import os

class FullscreenPreview(QWidget):
    def __init__(self, image_path, core=None, parent=None):
        super().__init__(parent)
        self.core = core
        self.image_path = image_path
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setStyleSheet("background-color: rgba(10, 10, 10, 0.98);")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Top overlay
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(20, 20, 20, 0)
        
        self.info_lbl = QLabel(os.path.basename(self.image_path))
        self.info_lbl.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        
        close_btn = QPushButton("✕")
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton { background-color: transparent; color: #a0a0a0; font-size: 24px; border: none;}
            QPushButton:hover { color: #ffffff; }
        """)
        close_btn.clicked.connect(self.close)
        
        top_layout.addWidget(self.info_lbl)
        top_layout.addStretch()
        top_layout.addWidget(close_btn)
        
        # Image
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Bottom controls overlay
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 30)
        bottom_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.set_btn = QPushButton("Set as Wallpaper")
        self.set_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.set_btn.setStyleSheet("""
            QPushButton { 
                background-color: #0078D4; color: white; border: none; 
                border-radius: 20px; padding: 12px 30px; font-weight: bold; font-size: 14px;
            }
            QPushButton:hover { background-color: #1084ea; }
        """)
        if self.core:
            self.set_btn.clicked.connect(self.set_wallpaper)
        else:
            self.set_btn.setVisible(False)
            
        is_fav = False
        if self.core:
            is_fav = self.core.db.is_favorite(self.image_path)
            
        self.fav_btn = QPushButton("★ Unfavorite" if is_fav else "☆ Favorite")
        self.fav_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.fav_btn.setStyleSheet("""
            QPushButton { 
                background-color: rgba(255, 255, 255, 0.1); color: white; border: 1px solid rgba(255,255,255,0.2); 
                border-radius: 20px; padding: 12px 30px; font-weight: bold; font-size: 14px;
                margin-right: 15px;
            }
            QPushButton:hover { background-color: rgba(255, 255, 255, 0.2); }
        """)
        if self.core:
            self.fav_btn.clicked.connect(self.toggle_favorite)
        else:
            self.fav_btn.setVisible(False)
            
        bottom_layout.addWidget(self.fav_btn)
            
        bottom_layout.addWidget(self.set_btn)
        
        layout.addLayout(top_layout)
        layout.addWidget(self.image_label, stretch=1)
        layout.addLayout(bottom_layout)
        
        self.setLayout(layout)
        
        # Esc to close
        self.shortcut = QShortcut(QKeySequence("Esc"), self)
        self.shortcut.activated.connect(self.close)
        
    def showEvent(self, event):
        super().showEvent(event)
        pixmap = QPixmap(self.image_path)
        if not pixmap.isNull():
            screen = self.screen().geometry()
            # Original quality edge-to-edge calculation (contain mode)
            pixmap = pixmap.scaled(screen.width() - 80, screen.height() - 150, 
                                   Qt.AspectRatioMode.KeepAspectRatio, 
                                   Qt.TransformationMode.SmoothTransformation)
            self.image_label.setPixmap(pixmap)
            
    def set_wallpaper(self):
        if self.core:
            if self.core.wallpaper_manager.set_specific_wallpaper(self.image_path):
                self.info_lbl.setText(f"{os.path.basename(self.image_path)} (Applied Successfully!)")
                self.info_lbl.setStyleSheet("color: #34d399; font-size: 16px; font-weight: bold;")
                self.set_btn.setText("Applied \u2713")
                self.set_btn.setStyleSheet("""
                    QPushButton { 
                        background-color: #10b981; color: white; border: none; 
                        border-radius: 20px; padding: 12px 30px; font-weight: bold; font-size: 14px;
                    }
                """)
                from PyQt6.QtCore import QTimer
                QTimer.singleShot(2000, self.reset_set_btn)

    def reset_set_btn(self):
        self.set_btn.setText("Set as Wallpaper")
        self.set_btn.setStyleSheet("""
            QPushButton { 
                background-color: #0078D4; color: white; border: none; 
                border-radius: 20px; padding: 12px 30px; font-weight: bold; font-size: 14px;
            }
            QPushButton:hover { background-color: #1084ea; }
        """)
        self.info_lbl.setText(os.path.basename(self.image_path))
        self.info_lbl.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")

    def toggle_favorite(self):
        if self.core:
            is_fav = self.core.db.is_favorite(self.image_path)
            if is_fav:
                self.core.db.remove_favorite(self.image_path)
                self.fav_btn.setText("☆ Favorite")
            else:
                self.core.db.add_favorite(self.image_path)
                self.fav_btn.setText("★ Unfavorite")
