import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QLabel, QFrame, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

class HistoryItem(QFrame):
    def __init__(self, wallpaper_path, timestamp, parent_core):
        super().__init__()
        self.core = parent_core
        self.setObjectName("card")
        self.setFixedHeight(90)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        
        thumb = QLabel()
        thumb.setFixedSize(110, 70)
        thumb.setStyleSheet("border-radius: 8px; background-color: #1e293b;")
        if os.path.exists(wallpaper_path):
            pix = QPixmap(wallpaper_path).scaled(110, 70, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
            thumb.setPixmap(pix)
            
        info_layout = QVBoxLayout()
        name_lbl = QLabel(os.path.basename(wallpaper_path))
        name_lbl.setStyleSheet("font-weight: 600; font-size: 14px; color: #e2e8f0; font-family: 'Segoe UI Variable Display', sans-serif;")
        
        time_str = timestamp.strftime('%Y-%m-%d %I:%M %p') if hasattr(timestamp, 'strftime') else timestamp
        time_lbl = QLabel(f"Applied: {time_str}")
        time_lbl.setStyleSheet("color: #64748b; font-size: 12px; font-family: 'Segoe UI Variable Text', sans-serif;")
        
        info_layout.addWidget(name_lbl)
        info_layout.addWidget(time_lbl)
        info_layout.addStretch()
        
        self.wallpaper_path = wallpaper_path
        self.apply_btn = QPushButton("Reapply")
        self.apply_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.apply_btn.clicked.connect(self.on_reapply_clicked)
        
        layout.addWidget(thumb)
        layout.addSpacing(15)
        layout.addLayout(info_layout, stretch=1)
        layout.addWidget(self.apply_btn)

    def on_reapply_clicked(self):
        success = self.core.wallpaper_manager.set_specific_wallpaper(self.wallpaper_path)
        if success:
            self.apply_btn.setText("Applied!")
            self.apply_btn.setStyleSheet("background-color: #10b981; color: white; border: none;")
        else:
            self.apply_btn.setText("Failed")
            self.apply_btn.setStyleSheet("background-color: #ef4444; color: white; border: none;")
            
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(2000, self.reset_btn)

    def reset_btn(self):
        self.apply_btn.setText("Reapply")
        self.apply_btn.setStyleSheet("")


class HistoryTab(QWidget):
    def __init__(self, core):
        super().__init__()
        self.core = core
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        header = QLabel("History")
        header.setObjectName("title")
        layout.addWidget(header)
        
        sub = QLabel("Your recently applied wallpapers and theme activities.")
        sub.setObjectName("subtitle")
        layout.addWidget(sub)
        
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border: none; background: transparent;")
        
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background: transparent;")
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.content_layout.setSpacing(10)
        self.scroll.setWidget(self.content_widget)
        
        layout.addWidget(self.scroll)
        
    def load_data(self):
        # Clear layout
        for i in reversed(range(self.content_layout.count())): 
            w = self.content_layout.itemAt(i).widget()
            if w:
                w.setParent(None)
            
        hist = self.core.db.get_history(50)
        
        if not hist:
            empty = QLabel("No history available yet. Your desktop wallpapers will appear here.")
            empty.setStyleSheet("color: #64748b; font-size: 14px; margin-top: 20px;")
            self.content_layout.addWidget(empty)
            return
            
        for item in hist:
            card = HistoryItem(item['file_path'], item['changed_time'], self.core)
            self.content_layout.addWidget(card)
