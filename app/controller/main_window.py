from PyQt6.QtWidgets import QMainWindow, QFileDialog
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QShortcut, QKeySequence
from app.player.vlc_player import VLCPlayer
from app.ui.ui_mainwindow import Ui_MainWindow
from app.counter.counter_manager import CounterManager
from app.counter.vehicle_data import VEHICLE_CLASSES
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtCore import Qt
class MainWindow(QMainWindow):
    """Main application window for Vehicle Traffic Counter.

    Wraps the generated UI (`Ui_MainWindow`) and exposes playback
    controls that use `VLCPlayer` to play video inside the UI's
    `videoFrame` widget.
    """

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.player = VLCPlayer(self.ui.videoFrame)
        self.counter = CounterManager()
        self.timer = QTimer(self)
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.update_ui)
        self.shortcut_space = QShortcut(QKeySequence("Space"), self)
        self.shortcut_space.setContext(Qt.ShortcutContext.ApplicationShortcut)
        self.shortcut_space.activated.connect(self.play_pause)
        self.shortcut_right = QShortcut(QKeySequence("Right"), self)
        self.shortcut_right.setContext(Qt.ShortcutContext.ApplicationShortcut)
        self.shortcut_right.activated.connect(self.next_frame)
        self.shortcut_left = QShortcut(QKeySequence("Left"), self)
        self.shortcut_left.setContext(Qt.ShortcutContext.ApplicationShortcut)
        self.shortcut_left.activated.connect(self.previous_frame)
        self.initialize_ui()
        self.setup_counter_table()
        self.connect_signals()

    def initialize_ui(self):
        self.setWindowTitle("Vehicle Traffic Counter")
        self.resize(1000, 700)
        self.setMinimumSize(900, 600)
        self.ui.sliderTimeline.setRange(0, 100)
        self.ui.lblCurrentTime.setText("00:00:00")
        self.ui.lblDuration.setText("00:00:00")
    
    def setup_counter_table(self):

        table = self.ui.tableCounter

        table.setRowCount(1)
        table.setColumnCount(len(VEHICLE_CLASSES))

        table.setHorizontalHeaderLabels(VEHICLE_CLASSES)

        for col in range(len(VEHICLE_CLASSES)):
            table.setItem(
                0,
                col,
                QTableWidgetItem("0")
            )

        table.verticalHeader().hide()

    def update_counter_table(self):
        counts = self.counter.get_counts()
        table = self.ui.tableCounter

        for col, vehicle in enumerate(VEHICLE_CLASSES):
            item = table.item(0, col)
            if item is None:
                item = QTableWidgetItem(str(counts.get(vehicle, 0)))
                table.setItem(0, col, item)
            else:
                item.setText(str(counts.get(vehicle, 0)))

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
        self.ui.actionPrevious_Frame.triggered.connect(self.previous_frame)
        self.ui.btnPrevFrame.clicked.connect(self.previous_frame)
        self.ui.btnNextFrame.clicked.connect(self.next_frame)
        self.ui.btnReset.clicked.connect(self.reset_counter)

    def open_video(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Video",
            "",
            "Video Files (*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.dav)"
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

    def previous_frame(self):
        """Step video playback backward by one frame."""
        self.player.previous_frame()

    def next_frame(self):
        """Step video playback forward by one frame."""
        self.player.next_frame()

    def play_pause(self):
        if self.player.is_playing():
            self.pause_video()
        else:
            self.play_video()

    def keyPressEvent(self, event):
         if (
                event.modifiers() == Qt.KeyboardModifier.ControlModifier
                and event.key() == Qt.Key.Key_Z
            ):
                self.counter.undo()
                self.update_counter_table()
                return

         key_map = {
             Qt.Key.Key_1: "Auto Rickshaw",
             Qt.Key.Key_2: "Bicycle",
             Qt.Key.Key_3: "Car",
             Qt.Key.Key_4: "Cycle Rickshaw",
             Qt.Key.Key_5: "Large Bus",
             Qt.Key.Key_6: "Mini Bus",
             Qt.Key.Key_7: "Micro Bus",
             Qt.Key.Key_8: "Heavy Truck",
             Qt.Key.Key_9: "Medium Truck",
             Qt.Key.Key_Q: "Small Truck",
             Qt.Key.Key_W: "Motorcycle",
             Qt.Key.Key_E: "Utility",
             Qt.Key.Key_R: "Caravan"
         }

         if event.key() in key_map:

             vehicle = key_map[event.key()]

             self.counter.increment(vehicle)

             self.update_counter_table()

             return

         super().keyPressEvent(event)

    def reset_counter(self):
        self.counter.reset()
        self.update_counter_table()