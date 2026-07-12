from PyQt6.QtWidgets import QMainWindow
from app.ui.ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.connect_signals()

    def connect_signals(self):
        self.ui.pushButton.clicked.connect(self.open_video)
        self.ui.pushButton_2.clicked.connect(self.play_video)

    def open_video(self):
        print("Open clicked")

    def play_video(self):
        print("Play clicked")