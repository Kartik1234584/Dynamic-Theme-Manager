from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                             QHBoxLayout, QFrame, QGridLayout, QPushButton,
                             QGraphicsDropShadowEffect, QGraphicsBlurEffect)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QImageReader, QColor
from ui.fullscreen_preview import FullscreenPreview
import os

class StatCard(QFrame):
    def __init__(self, title, value, icon_text):
        super().__init__()
        self.setObjectName("stat_card")
        self.setFixedSize(180, 110)
        
        # Shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(self)
        
        # Top row: icon + title
        t_layout = QHBoxLayout()
        icon = QLabel(icon_text)
        icon.setStyleSheet("font-family: 'Segoe Fluent Icons'; font-size: 22px; color: #38bdf8; margin-right: 8px;")
        t_label = QLabel(title)
        t_label.setStyleSheet("color: #94a3b8; font-weight: 600; font-size: 13px; font-family: 'Segoe UI Variable Display', 'Segoe UI', sans-serif;")
        t_layout.addWidget(icon)
        t_layout.addWidget(t_label)
        t_layout.addStretch()
        
        # Value
        self.v_label = QLabel(str(value))
        self.v_label.setStyleSheet("font-size: 28px; font-weight: bold; color: white; margin-top: 5px;")
        
        layout.addLayout(t_layout)
        layout.addWidget(self.v_label)
        layout.addStretch()
        
    def update_value(self, new_value):
        self.v_label.setText(str(new_value))

class DashboardTab(QWidget):
    def __init__(self, app_core):
        super().__init__()
        self.core = app_core
        self.setup_ui()
        self.load_data()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)
        
        header = QLabel("Dashboard")
        header.setObjectName("title")
        layout.addWidget(header)
        
        # Stat Cards Grid
        self.stats_layout = QHBoxLayout()
        self.card_wallpapers = StatCard("Total Wallpapers", "0", "\uE8B9")
        self.card_themes = StatCard("Total Themes", "0", "\uE790")
        self.card_ms_themes = StatCard("Microsoft Themes", "0", "\uE8B7")
        self.card_timer = StatCard("Timer Activity", "Running", "\uE823")
        
        self.stats_layout.addWidget(self.card_wallpapers)
        self.stats_layout.addWidget(self.card_themes)
        self.stats_layout.addWidget(self.card_ms_themes)
        self.stats_layout.addWidget(self.card_timer)
        self.stats_layout.addStretch()
        layout.addLayout(self.stats_layout)
        
        # Main content area: Preview + Activity
        content_layout = QHBoxLayout()
        
        # Left: Preview
        preview_container = QFrame()
        preview_container.setObjectName("card")
        p_layout = QVBoxLayout(preview_container)
        
        p_header = QLabel("Current Wallpaper")
        p_header.setStyleSheet("font-weight: bold; font-size: 16px; color: white;")
        p_layout.addWidget(p_header)
        
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setMinimumSize(400, 250)
        self.preview_label.setStyleSheet("background-color: #0f172a; border-radius: 8px;")
        
        self.info_label = QLabel("No wallpaper active")
        self.info_label.setStyleSheet("color: #94a3b8; font-size: 12px; margin-top: 5px;")
        
        # Actions
        actions_layout = QHBoxLayout()
        self.next_btn = QPushButton("Next Wallpaper")
        self.next_btn.setObjectName("primary")
        self.next_btn.clicked.connect(self.core.force_next_wallpaper)
        
        self.toggle_timer_btn = QPushButton("Start Timer")
        self.toggle_timer_btn.clicked.connect(self.on_toggle_timer_clicked)
        
        self.fullscreen_btn = QPushButton("Fullscreen View")
        self.fullscreen_btn.clicked.connect(self.show_fullscreen)
        self.fullscreen_btn.setVisible(False)
        
        self.refresh_btn = QPushButton("Refresh Data")
        self.refresh_btn.clicked.connect(self.on_refresh_clicked)
        
        actions_layout.addWidget(self.refresh_btn)
        actions_layout.addWidget(self.toggle_timer_btn)
        actions_layout.addWidget(self.next_btn)
        actions_layout.addWidget(self.fullscreen_btn)
        actions_layout.addStretch()
        
        p_layout.addWidget(self.preview_label, stretch=1)
        p_layout.addWidget(self.info_label)
        p_layout.addLayout(actions_layout)
        
        # Right: Live Activity Panel
        activity_container = QFrame()
        activity_container.setObjectName("card")
        activity_container.setFixedWidth(300)
        a_layout = QVBoxLayout(activity_container)
        
        a_header = QLabel("Live Activity")
        a_header.setStyleSheet("font-weight: bold; font-size: 16px; color: white;")
        a_layout.addWidget(a_header)
        
        self.activity_log = QLabel("• System initialized\n• Ready for rotation")
        self.activity_log.setWordWrap(True)
        self.activity_log.setStyleSheet("color: #94a3b8; font-size: 13px; line-height: 1.5;")
        self.activity_log.setAlignment(Qt.AlignmentFlag.AlignTop)
        a_layout.addWidget(self.activity_log, stretch=1)
        
        content_layout.addWidget(preview_container, stretch=2)
        content_layout.addWidget(activity_container, stretch=1)
        
        layout.addLayout(content_layout, stretch=1)
        self.setLayout(layout)
        
    def on_toggle_timer_clicked(self):
        self.core.toggle_timer()
        self.load_data()
        
    def on_refresh_clicked(self):
        self.core.theme_scanner.scan_initial_themes()
        self.load_data()
        
        current_text = self.activity_log.text()
        self.activity_log.setText("• Data Refreshed Successfully!\n\n" + current_text)
        
    def load_data(self):
        w_count = self.core.db.count_wallpapers()
        t_count = len(self.core.db.get_all_categories())
        
        # Count MS themes
        cats = self.core.db.get_all_categories()
        ms_count = sum(1 for c in cats if c.get('source') == 'Windows')
        
        self.card_wallpapers.update_value(w_count)
        self.card_themes.update_value(t_count)
        self.card_ms_themes.update_value(ms_count)
        
        if self.core.timer_manager.is_running:
            self.card_timer.update_value("Running")
            self.toggle_timer_btn.setText("Stop Timer")
        else:
            self.card_timer.update_value("Stopped")
            self.toggle_timer_btn.setText("Start Timer")
            
        current = self.core.wallpaper_manager.current_wallpaper
        self.update_preview(current)
        
    def update_preview(self, path):
        if not path or not os.path.exists(path):
            self.fullscreen_btn.setVisible(False)
            return
            
        self.current_preview_path = path
        self.fullscreen_btn.setVisible(True)
            
        pixmap = QPixmap(path)
        if not pixmap.isNull():
            # Scale pixmap keeping aspect ratio
            scaled = pixmap.scaled(self.preview_label.width(), self.preview_label.height(), 
                                   Qt.AspectRatioMode.KeepAspectRatio, 
                                   Qt.TransformationMode.SmoothTransformation)
            self.preview_label.setPixmap(scaled)
            
            # File info
            filename = os.path.basename(path)
            res = f"{pixmap.width()}x{pixmap.height()}"
            self.info_label.setText(f"{filename} • {res}")
            
            # Update activity log
            hist = self.core.wallpaper_manager.history[-5:]
            log_text = "\n\n".join([f"• Changed to: {os.path.basename(p)}" for p in reversed(hist)])
            if not log_text:
                log_text = "• Waiting for rotation..."
            self.activity_log.setText(log_text)

    def show_fullscreen(self):
        if hasattr(self, 'current_preview_path'):
            self.fs_window = FullscreenPreview(self.current_preview_path, self.core)
            self.fs_window.showFullScreen()
