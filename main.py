import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QFile, QTextStream

from app.controller.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    # Load QSS stylesheet
    qss_path = os.path.join(os.path.dirname(__file__), "style.qss")
    if os.path.exists(qss_path):
        file = QFile(qss_path)
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            app.setStyleSheet(stream.readAll())
            file.close()

    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
