from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, 
                             QStackedWidget, QListWidget, QListWidgetItem,
                             QSystemTrayIcon, QMenu, QFrame)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QAction
from ui.dashboard_tab import DashboardTab
from ui.wallpapers_tab import WallpapersTab
from ui.themes_tab import ThemesTab
from ui.favorites_tab import FavoritesTab
from ui.scheduler_tab import SchedulerTab
from ui.history_tab import HistoryTab
from ui.settings_tab import SettingsTab
from ui.styles import PREMIUM_DARK
import os

class MainWindow(QMainWindow):
    def __init__(self, app_core):
        super().__init__()
        self.core = app_core
        
        self.setWindowTitle("Dynamic Theme Manager")
        self.setMinimumSize(1100, 750)
        self.setStyleSheet(PREMIUM_DARK)
        
        self.setup_ui()
        self.setup_tray()
        
        # Connect to core signals
        self.core.wallpaper_manager.wallpaper_changed.connect(self.on_wallpaper_changed)
        self.core.timer_manager.timeout.connect(self.on_timer_tick)
        self.core.theme_scanner.theme_imported.connect(self.show_theme_toast)
        
    def create_fluent_icon(self, unicode_char, color="#94a3b8"):
        from PyQt6.QtGui import QPainter, QColor, QFont
        from PyQt6.QtCore import QRect
        pixmap = QPixmap(24, 24)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        font = QFont("Segoe Fluent Icons", 14)
        painter.setFont(font)
        painter.setPen(QColor(color))
        painter.drawText(QRect(0, 0, 24, 24), Qt.AlignmentFlag.AlignCenter, unicode_char)
        painter.end()
        return QIcon(pixmap)

    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        root_layout = QVBoxLayout(main_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)
        
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # --- SIDEBAR ---
        sidebar_container = QFrame()
        sidebar_container.setObjectName("sidebar")
        sidebar_container.setFixedWidth(260)
        s_layout = QVBoxLayout(sidebar_container)
        s_layout.setContentsMargins(0, 30, 0, 0)
        s_layout.setSpacing(10)
        
        # Logo
        logo_layout = QHBoxLayout()
        logo_layout.setContentsMargins(20, 0, 0, 20)
        logo_icon = QLabel("\uE790")
        logo_icon.setStyleSheet("font-family: 'Segoe Fluent Icons'; font-size: 20px; color: #38bdf8;")
        logo_text = QLabel("Theme Manager")
        logo_text.setStyleSheet("font-size: 16px; font-weight: 800; color: #ffffff; letter-spacing: -0.5px;")
        logo_layout.addWidget(logo_icon)
        logo_layout.addWidget(logo_text)
        logo_layout.addStretch()
        s_layout.addLayout(logo_layout)
        
        # Navigation
        self.sidebar = QListWidget()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setIconSize(QSize(20, 20))
        
        nav_items = [
            ("\uE80F", "Dashboard", DashboardTab),
            ("\uE8B9", "Wallpapers", WallpapersTab),
            ("\uE790", "Themes", ThemesTab),
            ("\uE734", "Favorites", FavoritesTab),
            ("\uE787", "Scheduler", SchedulerTab),
            ("\uE81C", "History", HistoryTab),
            ("\uE713", "Settings", SettingsTab)
        ]
        
        self.stack = QStackedWidget()
        self.tabs = {}
        
        for icon_code, name, TabClass in nav_items:
            item = QListWidgetItem(name)
            item.setIcon(self.create_fluent_icon(icon_code))
            item.setSizeHint(QSize(0, 45))
            self.sidebar.addItem(item)
            
            if TabClass:
                tab_widget = TabClass(self.core)
            else:
                # Premium Empty State
                tab_widget = QWidget()
                l = QVBoxLayout(tab_widget)
                empty_lbl = QLabel(f"<span style='font-family: \"Segoe Fluent Icons\"; font-size: 40px; color: #38bdf8;'>{icon_code}</span><br><br><b>{name}</b><br><br>This premium feature is currently being designed.<br>Coming in the next update!")
                empty_lbl.setStyleSheet("color: #64748b; font-size: 14px; text-align: center;")
                empty_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                l.addWidget(empty_lbl)
                
            self.tabs[name] = tab_widget
            self.stack.addWidget(tab_widget)
            
        self.sidebar.setCurrentRow(0)
        self.sidebar.currentRowChanged.connect(self.change_tab)
        s_layout.addWidget(self.sidebar)
        
        main_layout.addWidget(sidebar_container)
        main_layout.addWidget(self.stack)
        
        root_layout.addLayout(main_layout)
        
        # --- APP FOOTER ---
        footer_container = QWidget()
        footer_container_layout = QVBoxLayout(footer_container)
        footer_container_layout.setContentsMargins(10, 0, 10, 0)
        footer_container_layout.setSpacing(0)
        
        app_footer = QFrame()
        app_footer.setObjectName("app_footer")
        app_footer.setFixedHeight(36)
        
        footer_layout = QHBoxLayout(app_footer)
        footer_layout.setContentsMargins(20, 0, 20, 0)
        footer_layout.setSpacing(15)
        
        # Left Side
        left_layout = QHBoxLayout()
        left_layout.setContentsMargins(0,0,0,0)
        left_layout.setSpacing(8)
        
        status_dot = QLabel("●")
        status_dot.setStyleSheet("color: #10b981; font-size: 10px;") # Emerald green
        
        app_name = QLabel("Dynamic Theme Manager")
        app_name.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: 500;")
        
        left_layout.addWidget(status_dot)
        left_layout.addWidget(app_name)
        
        # Center Side
        center_layout = QHBoxLayout()
        center_layout.setContentsMargins(0,0,0,0)
        center_layout.setSpacing(4)
        
        dev_prefix = QLabel("Developed by")
        dev_prefix.setStyleSheet("color: #64748b; font-size: 11px;")
        
        self.dev_name = QLabel("Kartik Sadhu")
        self.dev_name.setObjectName("dev_name")
        self.dev_name.setCursor(Qt.CursorShape.PointingHandCursor)
        
        center_layout.addStretch()
        center_layout.addWidget(dev_prefix)
        center_layout.addWidget(self.dev_name)
        center_layout.addStretch()
        
        # Right Side
        right_layout = QHBoxLayout()
        right_layout.setContentsMargins(0,0,0,0)
        right_layout.setSpacing(10)
        
        active_theme = self.core.settings.get("last_theme")
        self.active_theme_lbl = QLabel(f"Active: {active_theme}")
        self.active_theme_lbl.setStyleSheet("color: #64748b; font-size: 11px;")
        
        divider1 = QLabel("|")
        divider1.setStyleSheet("color: #334155; font-size: 10px;")
        
        self.sync_lbl = QLabel("Last Sync: Just now")
        self.sync_lbl.setStyleSheet("color: #64748b; font-size: 11px;")
        
        divider2 = QLabel("|")
        divider2.setStyleSheet("color: #334155; font-size: 10px;")
        
        version_lbl = QLabel("v3.0 Premium Edition")
        version_lbl.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: bold;")
        
        right_layout.addWidget(self.active_theme_lbl)
        right_layout.addWidget(divider1)
        right_layout.addWidget(self.sync_lbl)
        right_layout.addWidget(divider2)
        right_layout.addWidget(version_lbl)
        
        footer_layout.addLayout(left_layout)
        footer_layout.addLayout(center_layout)
        footer_layout.addLayout(right_layout)
        
        footer_container_layout.addWidget(app_footer)
        root_layout.addWidget(footer_container)
        
    def change_tab(self, index):
        self.stack.setCurrentIndex(index)
        
        # Trigger reload on the active tab to update stats or lists
        active_tab = self.stack.widget(index)
        if hasattr(active_tab, 'load_data'):
            active_tab.load_data()
        
    def setup_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        
        # Use an empty icon or default icon if none exists
        import sys
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "icon.png")
        
        if os.path.exists(icon_path):
            self.tray_icon.setIcon(QIcon(icon_path))
        else:
            # Fallback empty icon
            pixmap = QPixmap(32, 32)
            pixmap.fill(Qt.GlobalColor.transparent)
            self.tray_icon.setIcon(QIcon(pixmap))
            
        tray_menu = QMenu()
        
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)
        
        next_action = QAction("Next Wallpaper", self)
        next_action.triggered.connect(self.core.force_next_wallpaper)
        tray_menu.addAction(next_action)
        
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.close_app)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
        self.tray_icon.activated.connect(self.tray_icon_activated)
        
    def show_theme_toast(self, theme_name, count):
        self.tray_icon.showMessage(
            "New Microsoft Theme Detected!",
            f"Successfully synced '{theme_name}' with {count} raw 4K wallpapers.",
            QSystemTrayIcon.MessageIcon.Information,
            4000
        )

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            if self.isVisible():
                self.hide()
            else:
                self.show()
                self.activateWindow()

    def on_wallpaper_changed(self, path):
        # Update dashboard if it's the current tab
        dashboard = self.stack.widget(0)
        if hasattr(dashboard, 'update_preview'):
            dashboard.update_preview(path)
            
        # Update active theme label
        active_theme = self.core.settings.get("last_theme")
        self.active_theme_lbl.setText(f"Active: {active_theme}")
            
    def on_timer_tick(self):
        dashboard = self.stack.widget(0)
        if hasattr(dashboard, 'load_data'):
            dashboard.load_data()
            
    def close_app(self):
        self.tray_icon.hide()
        self.core.timer_manager.stop()
        from PyQt6.QtWidgets import QApplication
        QApplication.quit()
        
    def closeEvent(self, event):
        # Minimize to tray instead of closing
        if self.core.settings.get("start_on_startup"):
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "Dynamic Theme Manager",
                "Application minimized to system tray and continues running in the background.",
                QSystemTrayIcon.MessageIcon.Information,
                2000
            )
        else:
            self.close_app()
