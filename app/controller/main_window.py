from PyQt6.QtWidgets import QMainWindow, QFileDialog
from PyQt6.QtCore import QTimer

from app.player.vlc_player import VLCPlayer
from app.ui.ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.player = VLCPlayer(self.ui.videoFrame)
        self.timer = QTimer(self)
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.update_ui)

        self.initialize_ui()
        self.connect_signals()

    def initialize_ui(self):
        self.setWindowTitle("Vehicle Traffic Counter")
        self.resize(1000, 700)
        self.setMinimumSize(900, 600)
        self.ui.sliderTimeline.setRange(0, 100)
        self.ui.lblCurrentTime.setText("00:00:00")
        self.ui.lblDuration.setText("00:00:00")

    def connect_signals(self):
        self.ui.btnOpen.clicked.connect(self.open_video)
        self.ui.btnPlay.clicked.connect(self.play_video)
        self.ui.btnPause.clicked.connect(self.pause_video)
        self.ui.btnStop.clicked.connect(self.stop_video)
        self.ui.sliderTimeline.sliderMoved.connect(self.seek_video)

        self.ui.actionOpen_Video.triggered.connect(self.open_video)
        self.ui.actionPlay.triggered.connect(self.play_video)
        self.ui.actionPause.triggered.connect(self.pause_video)
        self.ui.actionStop.triggered.connect(self.stop_video)
        self.ui.btnPrevFrame.clicked.connect(self.previous_frame)
        self.ui.btnNextFrame.clicked.connect(self.next_frame)

    def open_video(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Video",
            "",
            "Video Files (*.mp4 *.avi *.mkv *.mov *.wmv *.flv)"
        )

        if file_path:
            self.player.open(file_path)
            self.player.play()
            self.timer.start()

    def play_video(self):
        self.player.play()
        self.timer.start()

    def pause_video(self):
        self.player.pause()

    def stop_video(self):
        self.player.stop()
        self.timer.stop()

    def update_ui(self):
        current = self.player.get_time()
        duration = self.player.get_length()

        if duration <= 0:
            return

        self.ui.sliderTimeline.blockSignals(True)
        self.ui.sliderTimeline.setMaximum(max(duration, 1))
        self.ui.sliderTimeline.setValue(current)
        self.ui.sliderTimeline.blockSignals(False)

        self.ui.lblCurrentTime.setText(self.format_time(current))
        self.ui.lblDuration.setText(self.format_time(duration))

    def format_time(self, ms):
        seconds = max(0, int(ms // 1000))
        minutes = seconds // 60
        hours = minutes // 60
        return f"{hours:02}:{minutes % 60:02}:{seconds % 60:02}"

    def seek_video(self, position):
        self.player.set_time(position)
    
    
    def previous_frame(self, fps=30):
        frame_time = int(1000 / fps)
        current= self.player.get_time()
        self.player.set_time(max(0, current - frame_time))

    