PREMIUM_DARK = """
QMainWindow {
    background-color: #0b0f19; /* Very dark charcoal/blue base */
}

QWidget {
    color: #e2e8f0;
    font-family: 'Segoe UI Variable Text', 'Inter', 'Segoe UI', sans-serif;
    font-size: 13px;
}

/* Sidebar Styling */
QListWidget#sidebar {
    background-color: rgba(20, 25, 35, 0.7);
    border-right: 1px solid rgba(255, 255, 255, 0.05);
    outline: none;
    padding: 10px 0;
}

QListWidget#sidebar::item {
    padding: 12px 20px;
    margin: 4px 15px;
    border-radius: 8px;
    color: #94a3b8;
    font-family: 'Segoe UI Variable Display', 'Inter', sans-serif;
    font-weight: 500;
    font-size: 14px;
}

QListWidget#sidebar::item:hover {
    background-color: rgba(255, 255, 255, 0.05);
    color: #e2e8f0;
}

QListWidget#sidebar::item:selected {
    background-color: rgba(56, 189, 248, 0.15); /* Soft glowing blue */
    color: #38bdf8;
    border-left: 4px solid #38bdf8;
    font-weight: bold;
}

/* Scroll Area & Container */
QScrollArea {
    background-color: transparent;
    border: none;
}
QScrollArea > QWidget > QWidget {
    background-color: transparent;
}

/* Scrollbar */
QScrollBar:vertical {
    border: none;
    background: transparent;
    width: 6px;
    margin: 0;
}
QScrollBar::handle:vertical {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 3px;
    min-height: 20px;
}
QScrollBar::handle:vertical:hover {
    background: rgba(255, 255, 255, 0.2);
}

/* Headings */
QLabel#title {
    font-family: 'Segoe UI Variable Display', 'Inter', sans-serif;
    font-size: 28px;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.5px;
    margin-bottom: 5px;
}
QLabel#subtitle {
    font-family: 'Segoe UI Variable Text', 'Inter', sans-serif;
    font-size: 14px;
    color: #94a3b8;
    margin-bottom: 24px;
    line-height: 1.4;
}

/* Stat Cards / Content Cards */
QFrame#card, QFrame#stat_card {
    background-color: rgba(30, 41, 59, 0.5);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.03);
}
QFrame#card:hover, QFrame#stat_card:hover {
    background-color: rgba(30, 41, 59, 0.8);
    border: 1px solid rgba(56, 189, 248, 0.3);
}

/* Buttons */
QPushButton {
    background-color: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #e2e8f0;
    padding: 8px 18px;
    border-radius: 8px;
    font-family: 'Segoe UI Variable Text', 'Inter', sans-serif;
    font-weight: 600;
    font-size: 13px;
}
QPushButton:hover {
    background-color: rgba(255, 255, 255, 0.1);
}
QPushButton#primary {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0ea5e9, stop:1 #38bdf8);
    color: white;
    border: none;
}
QPushButton#primary:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0284c7, stop:1 #0ea5e9);
}

/* Inputs */
QLineEdit {
    background-color: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    padding: 8px 12px;
    color: white;
    font-size: 13px;
}
QLineEdit:focus {
    border: 1px solid #38bdf8;
    background-color: rgba(15, 23, 42, 0.8);
}

/* Combobox */
QComboBox {
    background-color: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    padding: 8px 12px;
    color: white;
}
QComboBox::drop-down {
    border: none;
    width: 20px;
}
QComboBox:hover {
    background-color: rgba(255, 255, 255, 0.05);
}

/* GroupBox */
QGroupBox {
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    margin-top: 15px;
    padding-top: 20px;
    font-weight: bold;
    color: #38bdf8;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 10px;
    left: 10px;
}

/* Tooltip */
QToolTip {
    background-color: #0f172a;
    color: #e2e8f0;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 4px;
    padding: 5px;
}

/* QMessageBox */
QMessageBox {
    background-color: #0f172a;
}
QMessageBox QLabel {
    color: #e2e8f0;
    font-size: 13px;
}
QMessageBox QPushButton {
    min-width: 80px;
    background-color: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: white;
}
QMessageBox QPushButton:hover {
    background-color: rgba(255, 255, 255, 0.1);
}

/* App Footer */
QFrame#app_footer {
    background-color: rgba(20, 25, 35, 0.85); /* Dark transparent, acrylic-like */
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    border-left: 1px solid rgba(255, 255, 255, 0.03);
    border-right: 1px solid rgba(255, 255, 255, 0.03);
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
}

QLabel#dev_name {
    color: #38bdf8;
    font-weight: bold;
    font-size: 11px;
    padding: 2px 6px;
    border-radius: 4px;
    background-color: transparent;
}

QLabel#dev_name:hover {
    color: #ffffff;
    background-color: rgba(56, 189, 248, 0.15);
}
"""
