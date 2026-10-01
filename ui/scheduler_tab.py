from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, 
                             QHBoxLayout, QComboBox, QCheckBox, QPushButton)
from PyQt6.QtCore import Qt

class SchedulerTab(QWidget):
    def __init__(self, core):
        super().__init__()
        self.core = core
        self.setup_ui()
        self.load_data()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        header = QLabel("Scheduler")
        header.setObjectName("title")
        layout.addWidget(header)
        
        sub = QLabel("Advanced time-of-day automation rules for your wallpapers.")
        sub.setObjectName("subtitle")
        layout.addWidget(sub)
        
        # Main Settings Card
        card = QFrame()
        card.setObjectName("card")
        card.setStyleSheet("background: rgba(30,41,59,0.5); padding: 20px; border-radius: 12px;")
        c_layout = QVBoxLayout(card)
        
        # Title and Toggle
        t_layout = QHBoxLayout()
        icon = QLabel("\uE787")
        icon.setStyleSheet("font-family: 'Segoe Fluent Icons'; font-size: 24px; color: #38bdf8; margin-right: 10px;")
        t = QLabel("Time-of-Day Rotation Profile")
        t.setStyleSheet("font-size: 16px; font-weight: 700; color: #e2e8f0; font-family: 'Segoe UI Variable Display', sans-serif;")
        
        self.enable_cb = QCheckBox("Enable Time-Based Scheduling")
        self.enable_cb.setStyleSheet("color: #e2e8f0; font-weight: bold;")
        self.enable_cb.stateChanged.connect(self.on_settings_changed)
        
        t_layout.addWidget(icon)
        t_layout.addWidget(t)
        t_layout.addStretch()
        t_layout.addWidget(self.enable_cb)
        
        c_layout.addLayout(t_layout)
        
        desc = QLabel("If enabled, the app will override your 'Active Theme' depending on the time of day.\n(Morning: 6 AM-12 PM, Afternoon: 12 PM-6 PM, Evening: 6 PM-10 PM, Night: 10 PM-6 AM)")
        desc.setStyleSheet("color: #94a3b8; font-size: 13px; margin-top: 10px; line-height: 1.5;")
        c_layout.addWidget(desc)
        
        # Selectors
        self.selectors = {}
        periods = [
            ("morning", "Morning Theme (06:00 - 12:00)"),
            ("afternoon", "Afternoon Theme (12:00 - 18:00)"),
            ("evening", "Evening Theme (18:00 - 22:00)"),
            ("night", "Night Theme (22:00 - 06:00)")
        ]
        
        for key, label_text in periods:
            row = QHBoxLayout()
            lbl = QLabel(label_text)
            lbl.setStyleSheet("color: #cbd5e1; font-weight: 500;")
            lbl.setFixedWidth(250)
            
            cb = QComboBox()
            cb.setFixedWidth(200)
            cb.currentIndexChanged.connect(self.on_settings_changed)
            
            self.selectors[key] = cb
            
            row.addWidget(lbl)
            row.addWidget(cb)
            row.addStretch()
            c_layout.addLayout(row)
            
        layout.addWidget(card)
        layout.addStretch()
        
    def load_data(self):
        # Prevent signals during load
        self.enable_cb.blockSignals(True)
        for cb in self.selectors.values():
            cb.blockSignals(True)
            
        # Populate comboboxes
        categories = self.core.db.get_all_categories()
        cat_names = [c["name"] for c in categories]
        
        settings = self.core.scheduler_manager.settings
        
        self.enable_cb.setChecked(settings.get("enabled", False))
        
        for key, cb in self.selectors.items():
            cb.clear()
            cb.addItems(["Random"] + cat_names)
            
            val = settings.get(key, "Random")
            if val in cat_names or val == "Random":
                cb.setCurrentText(val)
                
        # Restore signals
        self.enable_cb.blockSignals(False)
        for cb in self.selectors.values():
            cb.blockSignals(False)
            
    def on_settings_changed(self):
        settings = {
            "enabled": self.enable_cb.isChecked(),
            "morning": self.selectors["morning"].currentText(),
            "afternoon": self.selectors["afternoon"].currentText(),
            "evening": self.selectors["evening"].currentText(),
            "night": self.selectors["night"].currentText()
        }
        self.core.scheduler_manager.save_settings(settings)
