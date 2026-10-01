from PyQt6.QtWidgets import QCheckBox
from PyQt6.QtCore import Qt, QPropertyAnimation, pyqtProperty, QPoint
from PyQt6.QtGui import QPainter, QColor

class ToggleSwitch(QCheckBox):
    """A modern, animated toggle switch."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(45, 24)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._thumb_position = 2.0
        
        self.animation = QPropertyAnimation(self, b"thumb_position", self)
        self.animation.setDuration(200)
        self.stateChanged.connect(self.setup_animation)
        
        # We need to set initial position correctly based on initial state
        if self.isChecked():
            self._thumb_position = float(self.width() - 22)

    @pyqtProperty(float)
    def thumb_position(self):
        return self._thumb_position

    @thumb_position.setter
    def thumb_position(self, pos):
        self._thumb_position = pos
        self.update()

    def setup_animation(self, state):
        self.animation.stop()
        if state:
            self.animation.setEndValue(float(self.width() - 22))
        else:
            self.animation.setEndValue(2.0)
        self.animation.start()

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw track
        track_color = QColor("#0078D4") if self.isChecked() else QColor("#3d3d3d")
        p.setBrush(track_color)
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(0, 0, self.width(), self.height(), 12, 12)

        # Draw thumb
        p.setBrush(QColor("#ffffff"))
        p.drawEllipse(int(self._thumb_position), 2, 20, 20)
        
        p.end()
