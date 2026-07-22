import sys
import unittest

from PyQt6.QtWidgets import QApplication

from app.controller.main_window import MainWindow


class MainWindowShortcutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication(sys.argv)

    def setUp(self):
        self.window = MainWindow()

    def test_counter_shortcut_increments_vehicle(self):
        self.window._handle_counter_key(self._make_event("1", 0))
        self.assertEqual(
            self.window.counter.get_counts().get("Bicycle"), 1
        )

    def test_counter_shortcut_decrements_vehicle_with_shift(self):
        self.window.counter.set_count("Cart", 5)
        self.window._handle_counter_key(self._make_event("q", 0x02000000))
        self.assertEqual(self.window.counter.get_counts().get("Cart"), 4)

    def test_counter_shortcut_unknown_key_returns_none(self):
        result = self.window._handle_counter_key(self._make_event("z", 0))
        self.assertFalse(result)

    def _make_event(self, text, modifiers):
        from PyQt6.QtCore import Qt
        from PyQt6.QtGui import QKeyEvent

        key = ord(text.upper())
        return QKeyEvent(
            QKeyEvent.Type.KeyPress,
            key,
            Qt.KeyboardModifier(modifiers),
            text.upper(),
        )


if __name__ == "__main__":
    unittest.main()
