import sys

from PyQt6.QtWidgets import QApplication

from app.controller.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Vehicle Traffic Counter")

    window = MainWindow()
    window.show()

    try:
        sys.exit(app.exec())
    except AttributeError:
        sys.exit(app.exec_())


if __name__ == "__main__":
    main()