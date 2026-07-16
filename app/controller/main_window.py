import csv
import os

from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QShortcut, QKeySequence, QAction
from app.player.vlc_player import VLCPlayer
from app.ui.ui_mainwindow import Ui_MainWindow
from app.counter.counter_manager import CounterManager
from app.counter.vehicle_data import VEHICLE_CLASSES
from app.models.session import CountingSession
from app.services.excel_export import ExcelExporter
from app.services.session_service import SessionService


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.player = VLCPlayer(self.ui.videoFrame)
        self.current_video = ""
        self.counter = CounterManager()
        self.timer = QTimer(self)
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.update_ui)
        self._fullscreen = False

        self.initialize_ui()
        self.setup_counter_table()
        self.connect_signals()
        self.setup_shortcuts()

    def initialize_ui(self):
        self.setWindowTitle("Vehicle Traffic Counter")
        self.setWindowState(Qt.WindowState.WindowMaximized)
        self.ui.timelineSlider.setRange(0, 100)
        self.ui.lblCurrentTime.setText("00:00:00")
        self.ui.lblDuration.setText("00:00:00")
        self.ui.rbIncoming.setChecked(True)

    def setup_counter_table(self):
        table = self.ui.tableWidget
        table.setRowCount(2)
        table.setColumnCount(len(VEHICLE_CLASSES) + 1)

        headers = list(VEHICLE_CLASSES) + ["Total"]
        table.setHorizontalHeaderLabels(headers)
        table.setVerticalHeaderLabels(["Count", "Direction"])

        for col in range(len(VEHICLE_CLASSES) + 1):
            table.setItem(0, col, QTableWidgetItem("0"))
        table.setItem(1, 0, QTableWidgetItem("--"))

        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.horizontalHeader().setStretchLastSection(True)

    def update_counter_table(self):
        incoming = self.counter.incoming
        outgoing = self.counter.outgoing
        table = self.ui.tableWidget

        total = 0
        for col, vehicle in enumerate(VEHICLE_CLASSES):
            count = incoming.get(vehicle, 0)
            item = table.item(0, col)
            if item is None:
                item = QTableWidgetItem(str(count))
                table.setItem(0, col, item)
            else:
                item.setText(str(count))
            total += count

        total_item = table.item(0, len(VEHICLE_CLASSES))
        if total_item is None:
            total_item = QTableWidgetItem(str(total))
            table.setItem(0, len(VEHICLE_CLASSES), total_item)
        else:
            total_item.setText(str(total))

        mode = self.counter.mode
        for col in range(len(VEHICLE_CLASSES) + 1):
            mode_item = table.item(1, col)
            if mode_item is None:
                mode_item = QTableWidgetItem(mode)
                table.setItem(1, col, mode_item)
            else:
                mode_item.setText(mode)

    def connect_signals(self):
        self.ui.btnOpenVideo.clicked.connect(self.open_video)
        self.ui.btnPlay.clicked.connect(self.play_video)
        self.ui.btnPause.clicked.connect(self.pause_video)
        self.ui.btnStop.clicked.connect(self.stop_video)
        self.ui.btnPrevFrame.clicked.connect(self.previous_frame)
        self.ui.btnNextFrame.clicked.connect(self.next_frame)
        self.ui.timelineSlider.sliderMoved.connect(self.seek_by_slider)
        self.ui.timelineSlider.sliderPressed.connect(self.on_slider_pressed)
        self.ui.timelineSlider.sliderReleased.connect(self.on_slider_released)

        self.ui.actionOpen_Video.triggered.connect(self.open_video)
        self.ui.actionOpen_Folder.triggered.connect(self.open_folder)
        self.ui.actionExport_CSV.triggered.connect(self.export_csv)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionPlay.triggered.connect(self.play_video)
        self.ui.actionPause.triggered.connect(self.pause_video)
        self.ui.actionStop.triggered.connect(self.stop_video)
        self.ui.actionPrevious_Frame.triggered.connect(self.previous_frame)
        self.ui.actionNext_Frame.triggered.connect(self.next_frame)
        self.ui.actionAbout.triggered.connect(self.show_about)

        self.ui.btnSave.clicked.connect(self.save_session)
        self.ui.btnExport.clicked.connect(self.export_counts)
        self.ui.btnReset.clicked.connect(self.reset_counter)
        self.ui.rbIncoming.toggled.connect(self.on_direction_changed)
        self.ui.rbOutgoing.toggled.connect(self.on_direction_changed)

    def setup_shortcuts(self):
        self.shortcut_space = QShortcut(QKeySequence("Space"), self)
        self.shortcut_space.setContext(Qt.ShortcutContext.ApplicationShortcut)
        self.shortcut_space.activated.connect(self.toggle_play_pause)

        self.shortcut_right = QShortcut(QKeySequence("Right"), self)
        self.shortcut_right.setContext(Qt.ShortcutContext.ApplicationShortcut)
        self.shortcut_right.activated.connect(self.next_frame)

        self.shortcut_left = QShortcut(QKeySequence("Left"), self)
        self.shortcut_left.setContext(Qt.ShortcutContext.ApplicationShortcut)
        self.shortcut_left.activated.connect(self.previous_frame)

        self.shortcut_up = QShortcut(QKeySequence("Up"), self)
        self.shortcut_up.setContext(Qt.ShortcutContext.ApplicationShortcut)
        self.shortcut_up.activated.connect(lambda: self.adjust_volume(5))

        self.shortcut_down = QShortcut(QKeySequence("Down"), self)
        self.shortcut_down.setContext(Qt.ShortcutContext.ApplicationShortcut)
        self.shortcut_down.activated.connect(lambda: self.adjust_volume(-5))

        self.shortcut_fullscreen = QShortcut(QKeySequence("F"), self)
        self.shortcut_fullscreen.setContext(Qt.ShortcutContext.ApplicationShortcut)
        self.shortcut_fullscreen.activated.connect(self.toggle_fullscreen)

        self.shortcut_escape = QShortcut(QKeySequence("Escape"), self)
        self.shortcut_escape.setContext(Qt.ShortcutContext.ApplicationShortcut)
        self.shortcut_escape.activated.connect(self.exit_fullscreen)

        self.shortcut_undo = QShortcut(QKeySequence("Ctrl+Z"), self)
        self.shortcut_undo.setContext(Qt.ShortcutContext.ApplicationShortcut)
        self.shortcut_undo.activated.connect(self.undo_last)

    def open_video(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Video",
            "",
            "Video Files (*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.dav);;All Files (*)"
        )
        if file_path:
            self._load_video(file_path)

    def open_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Open Folder", "")
        if not folder_path:
            return

        supported_extensions = (".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".dav")
        for entry in sorted(os.listdir(folder_path)):
            if entry.lower().endswith(supported_extensions):
                self._load_video(os.path.join(folder_path, entry))
                return

        QMessageBox.warning(self, "Open Folder", "No supported video file found in the selected folder.")

    def _load_video(self, file_path):
        self.current_video = file_path
        self.player.open(file_path)
        self.player.play()
        self.timer.start()
        self.ui.statusbar.showMessage(f"Loaded: {os.path.basename(file_path)}")

    def play_video(self):
        if not self.current_video:
            return
        if not self.player.is_playing():
            self.player.play()
            self.timer.start()

    def pause_video(self):
        if self.player.is_playing():
            self.player.pause()

    def stop_video(self):
        self.player.stop()
        self.timer.stop()
        self.ui.timelineSlider.setValue(0)
        self.ui.lblCurrentTime.setText("00:00:00")
        self.ui.lblDuration.setText("00:00:00")

    def toggle_play_pause(self):
        if not self.current_video:
            return
        self.player.play_pause()
        if self.player.is_playing():
            self.timer.start()

    def next_frame(self):
        if not self.current_video:
            return
        self.player.next_frame()
        self._sync_slider()

    def previous_frame(self):
        if not self.current_video:
            return
        self.player.previous_frame()
        self._sync_slider()

    def _sync_slider(self):
        current = self.player.get_time()
        duration = self.player.get_length()
        if duration > 0:
            self.ui.timelineSlider.blockSignals(True)
            self.ui.timelineSlider.setMaximum(max(duration, 1))
            self.ui.timelineSlider.setValue(current)
            self.ui.timelineSlider.blockSignals(False)
            self.ui.lblCurrentTime.setText(self.format_time(current))
            self.ui.lblDuration.setText(self.format_time(duration))

    def update_ui(self):
        current = self.player.get_time()
        duration = self.player.get_length()
        if duration <= 0:
            return
        self.ui.timelineSlider.blockSignals(True)
        self.ui.timelineSlider.setMaximum(max(duration, 1))
        self.ui.timelineSlider.setValue(current)
        self.ui.timelineSlider.blockSignals(False)
        self.ui.lblCurrentTime.setText(self.format_time(current))
        self.ui.lblDuration.setText(self.format_time(duration))

    def on_slider_pressed(self):
        self._was_playing = self.player.is_playing()
        if self._was_playing:
            self.player.pause()

    def on_slider_released(self):
        if self._was_playing:
            self.player.play()

    def seek_by_slider(self, position):
        self.player.set_time(position)

    def format_time(self, ms):
        seconds = max(0, int(ms // 1000))
        minutes = seconds // 60
        hours = minutes // 60
        return f"{hours:02}:{minutes % 60:02}:{seconds % 60:02}"

    def on_direction_changed(self):
        if self.ui.rbIncoming.isChecked():
            self.counter.set_mode("Incoming")
        else:
            self.counter.set_mode("Outgoing")
        self.update_counter_table()

    def adjust_volume(self, delta):
        vol = self.player.player.audio_get_volume()
        self.player.player.audio_set_volume(max(0, min(200, vol + delta)))

    def toggle_fullscreen(self):
        if self._fullscreen:
            self.showNormal()
            self.ui.menubar.show()
            self.ui.statusbar.show()
        else:
            self.showFullScreen()
            self.ui.menubar.hide()
            self.ui.statusbar.hide()
        self._fullscreen = not self._fullscreen

    def exit_fullscreen(self):
        if self._fullscreen:
            self.showNormal()
            self.ui.menubar.show()
            self.ui.statusbar.show()
            self._fullscreen = False

    def undo_last(self):
        self.counter.undo()
        self.update_counter_table()

    def save_session(self):
        if not self.current_video:
            QMessageBox.warning(self, "Save Session", "Open a video first before saving a session.")
            return

        filename, _ = QFileDialog.getSaveFileName(self, "Save Session", "", "JSON Files (*.json)")
        if not filename:
            return
        if not filename.lower().endswith(".json"):
            filename += ".json"

        session = CountingSession(
            video_path=self.current_video,
            incoming=self.counter.incoming.copy(),
            outgoing=self.counter.outgoing.copy(),
            notes=""
        )
        SessionService.save(session, filename)
        QMessageBox.information(self, "Save Session", f"Session saved to {filename}.")

    def export_counts(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Export Counts", "", "Excel Files (*.xlsx)")
        if not filename:
            return
        if not filename.lower().endswith(".xlsx"):
            filename += ".xlsx"
        ExcelExporter.export(self.counter, filename)
        QMessageBox.information(self, "Export", f"Counts exported to {filename}.")

    def export_csv(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Export CSV", "", "CSV Files (*.csv)")
        if not filename:
            return
        if not filename.lower().endswith(".csv"):
            filename += ".csv"

        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Vehicle", "Incoming", "Outgoing"])
            for vehicle in VEHICLE_CLASSES:
                writer.writerow([
                    vehicle,
                    self.counter.incoming.get(vehicle, 0),
                    self.counter.outgoing.get(vehicle, 0)
                ])

        QMessageBox.information(self, "Export CSV", f"Counts exported to {filename}.")

    def reset_counter(self):
        reply = QMessageBox.question(
            self, "Reset Counter",
            "Are you sure you want to reset all counts?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.counter.reset()
            self.update_counter_table()

    def show_about(self):
        QMessageBox.about(
            self,
            "About Vehicle Traffic Counter",
            "Vehicle Traffic Counter v1.0\n\n"
            "A professional desktop application for manual vehicle traffic counting.\n\n"
            "Powered by VLC and PyQt6."
        )

    def keyPressEvent(self, event):
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
            self.ui.statusbar.showMessage(
                f"{self.counter.mode}: {vehicle} +1 (Total: {sum(self.counter.get_counts().values())})",
                3000
            )
            return

        super().keyPressEvent(event)
