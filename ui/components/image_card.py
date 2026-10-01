import os
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtWidgets import QGraphicsDropShadowEffect

class ImageCard(QFrame):
    """A beautiful card to display themes or wallpapers with rounded corners and shadows."""
    def __init__(self, image_path, title, subtitle="", source="Custom"):
        super().__init__()
        self.setObjectName("card")
        self.setFixedSize(220, 180)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Add shadow
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.shadow.setOffset(0, 4)
        self.setGraphicsEffect(self.shadow)
        
        # Smooth hover glow animation
        self.anim = QPropertyAnimation(self.shadow, b"blurRadius")
        self.anim.setDuration(250)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Image
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("border-top-left-radius: 12px; border-top-right-radius: 12px;")
        
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(220, 120, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
                self.image_label.setPixmap(pixmap)
        else:
            self.image_label.setText("No Image")
            
        # Text container
        text_container = QFrame()
        text_container.setStyleSheet("background-color: transparent; padding: 10px;")
        t_layout = QVBoxLayout(text_container)
        t_layout.setContentsMargins(0, 0, 0, 0)
        
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-weight: 600; font-size: 14px; color: white;")
        
        self.subtitle_label = QLabel(subtitle)
        self.subtitle_label.setStyleSheet("font-size: 12px; color: #a0a0a0;")
        
        t_layout.addWidget(self.title_label)
        t_layout.addWidget(self.subtitle_label)
        
        if source == 'Windows':
            badge = QLabel("💠 Microsoft Store")
            badge.setStyleSheet("font-size: 10px; color: #0078D4; font-weight: bold;")
            t_layout.addWidget(badge)
            
        layout.addWidget(self.image_label)
        layout.addWidget(text_container)

    def enterEvent(self, event):
        self.anim.stop()
        self.anim.setStartValue(self.shadow.blurRadius())
        self.anim.setEndValue(35)
        self.anim.start()
        # Change shadow color to primary accent
        self.shadow.setColor(QColor(56, 189, 248, 120))
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self.anim.stop()
        self.anim.setStartValue(self.shadow.blurRadius())
        self.anim.setEndValue(15)
        self.anim.start()
        self.shadow.setColor(QColor(0, 0, 0, 80))
        super().leaveEvent(event)
