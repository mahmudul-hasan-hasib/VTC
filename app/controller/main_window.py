from PyQt6.QtWidgets import QMainWindow, QFileDialog

from app.ui.ui_mainwindow import Ui_MainWindow
from app.player.vlc_player import VLCPlayer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Create VLC player
        self.player = VLCPlayer(self.ui.videoFrame)

        self.initialize_ui()
        self.connect_signals()

    def initialize_ui(self):
        self.setWindowTitle("Vehicle Traffic Counter")

    def connect_signals(self):
        # Buttons
        self.ui.btnOpen.clicked.connect(self.open_video)
        self.ui.btnPlay.clicked.connect(self.play_video)
        self.ui.btnPause.clicked.connect(self.pause_video)
        self.ui.btnStop.clicked.connect(self.stop_video)

        # Menu Actions
        self.ui.actionOpen_Video.triggered.connect(self.open_video)
        self.ui.actionPlay.triggered.connect(self.play_video)
        self.ui.actionPause.triggered.connect(self.pause_video)
        self.ui.actionStop.triggered.connect(self.stop_video)

    def open_video(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Video",
            "",
            "Video Files (*.mp4 *.avi *.mkv *.mov *.wmv *.flv)"
        )

        if file_path:
            self.player.open(file_path)
            self.player.play()  # Start playing the video immediately after opening 

    def play_video(self):
        self.player.play()

    def pause_video(self):
        self.player.pause()

    def stop_video(self):
        self.player.stop()