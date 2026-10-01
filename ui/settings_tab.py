from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                             QHBoxLayout, QGroupBox, QComboBox, 
                             QPushButton, QFormLayout, QSpinBox, QFrame)
from PyQt6.QtCore import Qt, QTimer
from utils.windows_api import add_to_startup, remove_from_startup
from ui.components.switch import ToggleSwitch
import os
import sys

class SettingsCard(QFrame):
    def __init__(self, title, description, widget):
        super().__init__()
        self.widget = widget
        self.setStyleSheet("background-color: rgba(255,255,255,0.03); border-radius: 8px;")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        
        t = QLabel(title)
        t.setStyleSheet("font-weight: bold; font-size: 14px; color: #e2e8f0; border: none; background: transparent;")
        
        d = QLabel(description)
        d.setStyleSheet("color: #64748b; font-size: 12px; border: none; background: transparent;")
        
        text_layout.addWidget(t)
        text_layout.addWidget(d)
        
        layout.addLayout(text_layout)
        layout.addStretch()
        layout.addWidget(widget)

    def mousePressEvent(self, event):
        # Forward click to widget if it's a toggle
        if hasattr(self.widget, 'toggle'):
            self.widget.toggle()
        super().mousePressEvent(event)

class SettingsTab(QWidget):
    def __init__(self, app_core):
        super().__init__()
        self.core = app_core
        self.setup_ui()
        self.load_settings()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(10)
        
        header = QLabel("Personalization Settings")
        header.setObjectName("title")
        layout.addWidget(header)
        
        subtitle = QLabel("Configure behavior, performance, and appearance.")
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)
        
        # System Category
        sys_lbl = QLabel("System Integration")
        sys_lbl.setStyleSheet("font-size: 15px; font-weight: bold; color: #38bdf8; margin-top: 15px; margin-bottom: 5px;")
        layout.addWidget(sys_lbl)
        
        self.startup_cb = ToggleSwitch()
        self.startup_cb.stateChanged.connect(self.on_startup_changed)
        layout.addWidget(SettingsCard("Launch on Startup", "Automatically start Dynamic Theme Manager when Windows starts.", self.startup_cb))
        
        # Rotation Category
        rot_lbl = QLabel("Wallpaper Rotation Engine")
        rot_lbl.setStyleSheet("font-size: 15px; font-weight: bold; color: #38bdf8; margin-top: 15px; margin-bottom: 5px;")
        layout.addWidget(rot_lbl)
        
        self.random_mode_cb = ToggleSwitch()
        self.random_mode_cb.stateChanged.connect(self.on_setting_changed)
        layout.addWidget(SettingsCard("Shuffle Wallpapers", "Randomize wallpaper selection instead of sequential rotation.", self.random_mode_cb))
        
        # Interval
        self.interval_combo = QComboBox()
        self.interval_combo.addItems(["30 Seconds", "1 Minute", "5 Minutes", "10 Minutes", "30 Minutes", "1 Hour", "Custom..."])
        self.interval_combo.currentIndexChanged.connect(self.on_interval_changed)
        self.interval_combo.setFixedWidth(150)
        layout.addWidget(SettingsCard("Rotation Interval", "How frequently the desktop wallpaper automatically changes.", self.interval_combo))
        
        self.custom_spin = QSpinBox()
        self.custom_spin.setRange(10, 86400)
        self.custom_spin.setSuffix(" sec")
        self.custom_spin.setFixedWidth(150)
        self.custom_spin.setVisible(False)
        self.custom_spin.valueChanged.connect(self.on_setting_changed)
        self.custom_container = SettingsCard("Custom Interval", "Enter the exact number of seconds.", self.custom_spin)
        self.custom_container.setVisible(False)
        layout.addWidget(self.custom_container)
        
        # Theme Category
        th_lbl = QLabel("Active Synchronization")
        th_lbl.setStyleSheet("font-size: 15px; font-weight: bold; color: #38bdf8; margin-top: 15px; margin-bottom: 5px;")
        layout.addWidget(th_lbl)
        
        self.theme_combo = QComboBox()
        self.theme_combo.currentTextChanged.connect(self.on_setting_changed)
        self.theme_combo.setFixedWidth(150)
        layout.addWidget(SettingsCard("Default Theme Collection", "Select the starting theme category.", self.theme_combo))
        
        # Save Button
        save_btn = QPushButton("Save Config & Apply")
        save_btn.setObjectName("primary")
        save_btn.clicked.connect(self.save_settings)
        save_btn.setFixedSize(160, 40)
        
        layout.addStretch()
        layout.addWidget(save_btn, alignment=Qt.AlignmentFlag.AlignRight)
        
        self.setLayout(layout)
        
    def load_settings(self):
        categories = self.core.db.get_all_categories()
        self.theme_combo.clear()
        for cat in categories:
            self.theme_combo.addItem(cat['name'])
            
        settings = self.core.settings
        self.startup_cb.setChecked(settings.get("start_on_startup"))
        self.random_mode_cb.setChecked(settings.get("random_mode"))
        
        idx = self.theme_combo.findText(settings.get("last_theme"))
        if idx >= 0:
            self.theme_combo.setCurrentIndex(idx)
            
        interval = settings.get("timer_interval")
        interval_map = {30: 0, 60: 1, 300: 2, 600: 3, 1800: 4, 3600: 5}
        
        if interval in interval_map:
            self.interval_combo.setCurrentIndex(interval_map[interval])
            self.custom_container.setVisible(False)
        else:
            self.interval_combo.setCurrentIndex(6)
            self.custom_container.setVisible(True)
            self.custom_spin.setValue(interval)
            
    def on_interval_changed(self, index):
        if index == 6:
            self.custom_container.setVisible(True)
        else:
            self.custom_container.setVisible(False)
        self.on_setting_changed()
            
    def on_setting_changed(self):
        pass
        
    def on_startup_changed(self, state):
        app_name = "DynamicThemeManager"
        exe_path = sys.executable if sys.executable.endswith("exe") else os.path.abspath("main.py")
        if hasattr(sys, 'frozen'):
            exe_path = sys.executable
        else:
            exe_path = f'"{sys.executable}" "{os.path.abspath("main.py")}"'
            
        if state == 2:
            add_to_startup(app_name, exe_path)
        else:
            remove_from_startup(app_name)
            
    def save_settings(self):
        interval_map = [30, 60, 300, 600, 1800, 3600]
        idx = self.interval_combo.currentIndex()
        if idx < 6:
            interval = interval_map[idx]
        else:
            interval = self.custom_spin.value()
            
        self.core.settings.set("start_on_startup", self.startup_cb.isChecked())
        self.core.settings.set("random_mode", self.random_mode_cb.isChecked())
        self.core.settings.set("last_theme", self.theme_combo.currentText())
        self.core.settings.set("timer_interval", interval)
        self.core.apply_settings()
        
        # Provide visual feedback to the user
        btn = self.sender()
        if btn:
            original_text = btn.text()
            btn.setText("✓ Settings Saved!")
            btn.setStyleSheet("background-color: #22c55e; color: white; border: none; font-weight: bold;")
            QTimer.singleShot(2000, lambda: (btn.setText(original_text), btn.setStyleSheet("")))
