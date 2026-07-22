from PyQt6.QtCore import pyqtSignal, Qt, QRectF
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QBrush


class CounterWidget(QWidget):
    """Interactive count box: left-click +1, right-click -1, wheel +/-1."""

    valueChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 0
        self._hovered = False
        self.setFixedSize(80, 34)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMouseTracking(True)
        self.setToolTip("Left-click +1 | Right-click -1 | Scroll to change")

    def value(self):
        return self._value

    def setValue(self, val):
        v = max(0, val)
        if self._value != v:
            self._value = v
            self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._value += 1
            self.valueChanged.emit(self._value)
            self.update()
        elif event.button() == Qt.MouseButton.RightButton:
            if self._value > 0:
                self._value -= 1
                self.valueChanged.emit(self._value)
                self.update()

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self._value += 1
        elif self._value > 0:
            self._value -= 1
        self.valueChanged.emit(self._value)
        self.update()

    def enterEvent(self, event):
        self._hovered = True
        self.update()

    def leaveEvent(self, event):
        self._hovered = False
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = QRectF(self.rect()).adjusted(1, 1, -1, -1)

        alt = self.property("altRow")
        if self._hovered:
            bg = QColor("#2E6BFF")
        elif alt:
            bg = QColor("#1a2540")
        else:
            bg = QColor("#1F2945")

        painter.setBrush(QBrush(bg))
        painter.setPen(QPen(QColor("#2E6BFF"), 1))
        painter.drawRoundedRect(rect, 8, 8)

        font = QFont("Consolas", 13, QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(QColor("#ffffff"))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(self._value))

        painter.end()
