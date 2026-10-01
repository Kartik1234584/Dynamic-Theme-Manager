import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QLabel, QFrame, QPushButton
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from ui.components.flow_layout import FlowLayout

class FavoriteCard(QFrame):
    def __init__(self, path, name, core, parent_tab):
        super().__init__()
        self.core = core
        self.parent_tab = parent_tab
        self.path = path
        self.setObjectName("card")
        self.setFixedSize(220, 180)
        
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.shadow.setOffset(0, 4)
        self.setGraphicsEffect(self.shadow)
        
        self.anim = QPropertyAnimation(self.shadow, b"blurRadius")
        self.anim.setDuration(250)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        
        thumb = QLabel()
        thumb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        thumb.setStyleSheet("border-top-left-radius: 12px; border-top-right-radius: 12px; background: #1e293b;")
        if os.path.exists(path):
            pix = QPixmap(path).scaled(220, 120, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
            thumb.setPixmap(pix)
            
        text_container = QFrame()
        text_container.setStyleSheet("background: transparent; padding: 10px;")
        t_layout = QVBoxLayout(text_container)
        t_layout.setContentsMargins(0,0,0,0)
        
        n_lbl = QLabel(name)
        n_lbl.setStyleSheet("font-weight: 600; font-size: 13px; color: #e2e8f0; font-family: 'Segoe UI Variable Display', sans-serif;")
        t_layout.addWidget(n_lbl)
        
        actions = QHBoxLayout()
        self.apply_btn = QPushButton("Apply")
        self.apply_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.apply_btn.setStyleSheet("padding: 4px 8px; font-size: 11px;")
        self.apply_btn.clicked.connect(self.apply_wallpaper)
        
        rm_btn = QPushButton("Remove")
        rm_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        rm_btn.setStyleSheet("padding: 4px 8px; font-size: 11px; background-color: rgba(239, 68, 68, 0.2); color: #fca5a5; border: none;")
        rm_btn.clicked.connect(self.remove_fav)
        
        actions.addWidget(self.apply_btn)
        actions.addWidget(rm_btn)
        t_layout.addLayout(actions)
        
        layout.addWidget(thumb)
        layout.addWidget(text_container)

    def apply_wallpaper(self):
        if self.core.wallpaper_manager.set_specific_wallpaper(self.path):
            self.apply_btn.setText("Applied \u2713")
            self.apply_btn.setStyleSheet("padding: 4px 8px; font-size: 11px; background-color: rgba(16, 185, 129, 0.2); color: #34d399; border: none;")
            
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(2000, self.reset_apply_btn)
            
    def reset_apply_btn(self):
        self.apply_btn.setText("Apply")
        self.apply_btn.setStyleSheet("padding: 4px 8px; font-size: 11px;")

    def remove_fav(self):
        self.core.db.remove_favorite(self.path)
        self.parent_tab.load_data()

    def enterEvent(self, event):
        self.anim.stop()
        self.anim.setStartValue(self.shadow.blurRadius())
        self.anim.setEndValue(35)
        self.anim.start()
        self.shadow.setColor(QColor(56, 189, 248, 120))
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self.anim.stop()
        self.anim.setStartValue(self.shadow.blurRadius())
        self.anim.setEndValue(15)
        self.anim.start()
        self.shadow.setColor(QColor(0, 0, 0, 80))
        super().leaveEvent(event)

class FavoritesTab(QWidget):
    def __init__(self, core):
        super().__init__()
        self.core = core
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        header = QLabel("Favorites")
        header.setObjectName("title")
        layout.addWidget(header)
        
        sub = QLabel("Your personally curated collection of favorite wallpapers.")
        sub.setObjectName("subtitle")
        layout.addWidget(sub)
        
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border: none; background: transparent;")
        
        self.grid_widget = QWidget()
        self.grid_widget.setStyleSheet("background: transparent;")
        self.grid_layout = FlowLayout(self.grid_widget, margin=0, hSpacing=20, vSpacing=20)
        self.scroll.setWidget(self.grid_widget)
        
        layout.addWidget(self.scroll)
        
    def load_data(self):
        for i in reversed(range(self.grid_layout.count())): 
            w = self.grid_layout.itemAt(i).widget()
            if w: w.setParent(None)
            
        favs = self.core.db.get_favorites()
        if not favs:
            empty = QLabel("No favorites yet. Open a wallpaper in the gallery to favorite it!")
            empty.setStyleSheet("color: #64748b; font-size: 14px; margin-top: 20px;")
            self.grid_layout.addWidget(empty)
            return
            
        for f in favs:
            card = FavoriteCard(f['path'], f['filename'], self.core, self)
            self.grid_layout.addWidget(card)
