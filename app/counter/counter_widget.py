from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QSpinBox, QWidget


class CounterWidget(QWidget):
    """Reusable editable counter: [-] [SpinBox] [+]."""

    valueChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._updating = False

        self._btn_minus = QPushButton("\u2212", self)
        self._btn_minus.setObjectName("counterBtnMinus")
        self._btn_minus.setFixedSize(34, 34)
        self._btn_minus.setCursor(self._btn_minus.cursor())
        self._btn_minus.clicked.connect(self._decrement)

        self._spin = QSpinBox(self)
        self._spin.setObjectName("counterSpinBox")
        self._spin.setRange(0, 99999)
        self._spin.setFixedHeight(36)
        self._spin.setAlignment(self._spin.alignment())
        self._spin.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        self._spin.valueChanged.connect(self._on_value_changed)

        self._btn_plus = QPushButton("+", self)
        self._btn_plus.setObjectName("counterBtnPlus")
        self._btn_plus.setFixedSize(34, 34)
        self._btn_plus.setCursor(self._btn_plus.cursor())
        self._btn_plus.clicked.connect(self._increment)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(4)
        layout.addWidget(self._btn_minus)
        layout.addWidget(self._spin, 1)
        layout.addWidget(self._btn_plus)

        self._update_buttons()

    def value(self):
        return self._spin.value()

    def setValue(self, val):
        if self._spin.value() == val:
            return
        self._updating = True
        self._spin.setValue(val)
        self._updating = False
        self._update_buttons()

    def _on_value_changed(self, val):
        self._update_buttons()
        if not self._updating:
            self.valueChanged.emit(val)

    def _update_buttons(self):
        self._btn_minus.setEnabled(self._spin.value() > 0)

    def _increment(self):
        self._spin.setValue(self._spin.value() + 1)

    def _decrement(self):
        if self._spin.value() > 0:
            self._spin.setValue(self._spin.value() - 1)
