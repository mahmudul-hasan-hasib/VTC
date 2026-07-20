import csv
import os
from datetime import datetime

import vlc
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QMessageBox,
    QGridLayout, QLabel, QWidget,
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QShortcut, QKeySequence

from app.player.vlc_player import VLCPlayer
from app.ui.ui_mainwindow import Ui_MainWindow
from app.counter.counter_manager import CounterManager
from app.counter.vehicle_data import (
    VEHICLE_CLASSES, LEFT_COLUMN, RIGHT_COLUMN, KEY_VEHICLE_MAP,
)
from app.models.session import CountingSession
from app.services.excel_export import ExcelExporter
from app.services.session_service import SessionService

VEHICLE_KEY_MAP = {v: k for k, v in KEY_VEHICLE_MAP.items()}
BADGE_HTML = (
    '<span style="background-color:#0f3460;color:#ffffff;font-weight:bold;'
    'border-radius:3px;padding:1px 5px;font-size:10px;">{}</span>'
    '&nbsp;&nbsp;{}'
)
SPEEDS = [0.25, 0.50, 0.75, 1.00, 1.25, 1.50, 1.75, 2.00, 3.00, 4.00, 5.00, 6.00]
SPEED_LABELS = [f"{s:.2f}x" for s in SPEEDS]
DEFAULT_SPEED_INDEX = 3


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.player = VLCPlayer(self.ui.videoFrame)
        self.current_video = ""
        self.counter = CounterManager()
        self._fullscreen = False
        self._was_playing = False
        self._slider_pressed = False
        self._video_loaded = False
        self._current_speed_index = DEFAULT_SPEED_INDEX

        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self._on_timer_tick)

        self.initialize_ui()
        self.setup_counter_table()
        self.populate_speed_combo()
        self.connect_signals()
        self.setup_shortcuts()
        self._update_control_states()
        QApplication.instance().installEventFilter(self)

    # ------------------------------------------------------------------ init
    def initialize_ui(self):
        self.setWindowTitle("Vehicle Traffic Counter")
        self.setWindowState(Qt.WindowState.WindowMaximized)
        self.ui.timelineSlider.setRange(0, 1000)
        self.ui.timelineSlider.setValue(0)
        self.ui.lblCurrentTime.setText("00:00:00")
        self.ui.lblDuration.setText("00:00:00")
        self.ui.rbIncoming.setChecked(True)

    def populate_speed_combo(self):
        self.ui.speedCombo.addItems(SPEED_LABELS)
        self.ui.speedCombo.setCurrentIndex(DEFAULT_SPEED_INDEX)
        self.ui.speedCombo.setEnabled(False)

    def _update_control_states(self):
        enabled = self._video_loaded
        self.ui.btnPlay.setEnabled(enabled)
        self.ui.btnPause.setEnabled(enabled)
        self.ui.btnStop.setEnabled(enabled)
        self.ui.btnPrevFrame.setEnabled(enabled)
        self.ui.btnNextFrame.setEnabled(enabled)
        self.ui.timelineSlider.setEnabled(enabled)
        self.ui.speedCombo.setEnabled(enabled)
        self.ui.actionPlay.setEnabled(enabled)
        self.ui.actionPause.setEnabled(enabled)
        self.ui.actionStop.setEnabled(enabled)
        self.ui.actionPrevious_Frame.setEnabled(enabled)
        self.ui.actionNext_Frame.setEnabled(enabled)

    # ----------------------------------------------------------- counter table
    def setup_counter_table(self):
        widget = self.ui.counterWidget
        layout = QGridLayout(widget)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(0)

        h_left_name = QLabel("Vehicle")
        h_left_name.setObjectName("counterHeaderLabel")
        h_left_count = QLabel("Count")
        h_left_count.setObjectName("counterHeaderLabel")
        h_left_count.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        h_right_name = QLabel("Vehicle")
        h_right_name.setObjectName("counterHeaderLabel")
        h_right_count = QLabel("Count")
        h_right_count.setObjectName("counterHeaderLabel")
        h_right_count.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

        layout.addWidget(h_left_name, 0, 0)
        layout.addWidget(h_left_count, 0, 1)
        layout.addWidget(h_right_name, 0, 2)
        layout.addWidget(h_right_count, 0, 3)

        sep_top = QWidget()
        sep_top.setObjectName("counterSeparator")
        sep_top.setFixedHeight(1)
        layout.addWidget(sep_top, 1, 0, 1, 4)

        self._count_labels = {}
        max_rows = max(len(LEFT_COLUMN), len(RIGHT_COLUMN))

        for i in range(max_rows):
            grid_row = i + 2

            if i < len(LEFT_COLUMN):
                vehicle = LEFT_COLUMN[i]
                key = VEHICLE_KEY_MAP.get(vehicle, "")
                name_lbl = QLabel(BADGE_HTML.format(key, vehicle))
                name_lbl.setTextFormat(Qt.TextFormat.RichText)
                name_lbl.setObjectName("vehicleNameLabel")
                count_lbl = QLabel("0")
                count_lbl.setObjectName("vehicleCountLabel")
                count_lbl.setAlignment(
                    Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                )
                if grid_row % 2 == 0:
                    name_lbl.setProperty("altRow", True)
                    count_lbl.setProperty("altRow", True)
                layout.addWidget(name_lbl, grid_row, 0)
                layout.addWidget(count_lbl, grid_row, 1)
                self._count_labels[vehicle] = count_lbl

            if i < len(RIGHT_COLUMN):
                vehicle = RIGHT_COLUMN[i]
                key = VEHICLE_KEY_MAP.get(vehicle, "")
                name_lbl = QLabel(BADGE_HTML.format(key, vehicle))
                name_lbl.setTextFormat(Qt.TextFormat.RichText)
                name_lbl.setObjectName("vehicleNameLabel")
                count_lbl = QLabel("0")
                count_lbl.setObjectName("vehicleCountLabel")
                count_lbl.setAlignment(
                    Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                )
                if grid_row % 2 == 0:
                    name_lbl.setProperty("altRow", True)
                    count_lbl.setProperty("altRow", True)
                layout.addWidget(name_lbl, grid_row, 2)
                layout.addWidget(count_lbl, grid_row, 3)
                self._count_labels[vehicle] = count_lbl

        sep_bot = QWidget()
        sep_bot.setObjectName("counterSeparator")
        sep_bot.setFixedHeight(1)
        layout.addWidget(sep_bot, max_rows + 2, 0, 1, 4)

        total_name = QLabel("Total")
        total_name.setObjectName("totalLabel")
        self._total_label = QLabel("0")
        self._total_label.setObjectName("totalCountLabel")
        self._total_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

        layout.addWidget(total_name, max_rows + 3, 0, 1, 2)
        layout.addWidget(self._total_label, max_rows + 3, 2, 1, 2)

        layout.setColumnStretch(0, 3)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 3)
        layout.setColumnStretch(3, 1)

    def update_counter_table(self):
        counts = self.counter.get_counts()
        total = 0
        for vehicle, label in self._count_labels.items():
            count = counts.get(vehicle, 0)
            label.setText(str(count))
            total += count
        self._total_label.setText(str(total))

    # --------------------------------------------------------- signal wiring
    def connect_signals(self):
        self.ui.btnOpenVideo.clicked.connect(self.open_video)
        self.ui.btnPlay.clicked.connect(self.play_video)
        self.ui.btnPause.clicked.connect(self.pause_video)
        self.ui.btnStop.clicked.connect(self.stop_video)
        self.ui.btnPrevFrame.clicked.connect(self.previous_frame)
        self.ui.btnNextFrame.clicked.connect(self.next_frame)
        self.ui.timelineSlider.sliderMoved.connect(self._on_slider_moved)
        self.ui.timelineSlider.sliderPressed.connect(self._on_slider_pressed)
        self.ui.timelineSlider.sliderReleased.connect(self._on_slider_released)

        self.ui.speedCombo.currentIndexChanged.connect(self._on_speed_combo_changed)

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

        self.shortcut_ctrl_right = QShortcut(QKeySequence("Ctrl+Right"), self)
        self.shortcut_ctrl_right.setContext(Qt.ShortcutContext.ApplicationShortcut)
        self.shortcut_ctrl_right.activated.connect(lambda: self._seek_relative(5000))

        self.shortcut_ctrl_left = QShortcut(QKeySequence("Ctrl+Left"), self)
        self.shortcut_ctrl_left.setContext(Qt.ShortcutContext.ApplicationShortcut)
        self.shortcut_ctrl_left.activated.connect(lambda: self._seek_relative(-5000))

        self.shortcut_up = QShortcut(QKeySequence("Up"), self)
        self.shortcut_up.setContext(Qt.ShortcutContext.ApplicationShortcut)
        self.shortcut_up.activated.connect(self._speed_up)

        self.shortcut_down = QShortcut(QKeySequence("Down"), self)
        self.shortcut_down.setContext(Qt.ShortcutContext.ApplicationShortcut)
        self.shortcut_down.activated.connect(self._speed_down)

        self.shortcut_home = QShortcut(QKeySequence("Home"), self)
        self.shortcut_home.setContext(Qt.ShortcutContext.ApplicationShortcut)
        self.shortcut_home.activated.connect(self._go_to_start)

        self.shortcut_end = QShortcut(QKeySequence("End"), self)
        self.shortcut_end.setContext(Qt.ShortcutContext.ApplicationShortcut)
        self.shortcut_end.activated.connect(self._go_to_end)

        self.shortcut_fullscreen = QShortcut(QKeySequence("F"), self)
        self.shortcut_fullscreen.setContext(Qt.ShortcutContext.ApplicationShortcut)
        self.shortcut_fullscreen.activated.connect(self.toggle_fullscreen)

        self.shortcut_escape = QShortcut(QKeySequence("Escape"), self)
        self.shortcut_escape.setContext(Qt.ShortcutContext.ApplicationShortcut)
        self.shortcut_escape.activated.connect(self.exit_fullscreen)

        self.shortcut_undo = QShortcut(QKeySequence("Ctrl+Z"), self)
        self.shortcut_undo.setContext(Qt.ShortcutContext.ApplicationShortcut)
        self.shortcut_undo.activated.connect(self.undo_last)

    # ----------------------------------------------------------- video open
    def open_video(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Video",
            "",
            "Video Files (*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.dav);;All Files (*)",
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
        QMessageBox.warning(
            self, "Open Folder", "No supported video file found in the selected folder."
        )

    def _load_video(self, file_path):
        try:
            self.timer.stop()
            self.player.stop()
            self.player.open(file_path)
            self.current_video = file_path
            self._video_loaded = True
            self._update_control_states()
            self.player.play()
            self.timer.start()
            self.ui.speedCombo.blockSignals(True)
            self.ui.speedCombo.setCurrentIndex(DEFAULT_SPEED_INDEX)
            self.ui.speedCombo.blockSignals(False)
            self._current_speed_index = DEFAULT_SPEED_INDEX
            self.ui.timelineSlider.blockSignals(True)
            self.ui.timelineSlider.setRange(0, 1000)
            self.ui.timelineSlider.setValue(0)
            self.ui.timelineSlider.blockSignals(False)
            self.ui.lblCurrentTime.setText("00:00:00")
            self.ui.lblDuration.setText("00:00:00")
            self.ui.statusbar.showMessage(f"Loaded: {os.path.basename(file_path)}")
            QTimer.singleShot(250, self._sync_initial_duration)
            QTimer.singleShot(250, self._sync_slider)
        except Exception as e:
            self._video_loaded = False
            self._update_control_states()
            QMessageBox.critical(
                self, "Error", f"Could not open video:\n{file_path}\n\n{e}"
            )

    def _sync_initial_duration(self):
        duration = self.player.get_length()
        if duration > 0:
            self.ui.timelineSlider.blockSignals(True)
            self.ui.timelineSlider.setMaximum(duration)
            self.ui.timelineSlider.blockSignals(False)
            self.ui.lblDuration.setText(self.format_time(duration))

    # ----------------------------------------------------------- playback
    def play_video(self):
        if not self._video_loaded:
            return
        self.player.play()
        self.timer.start()
        if self.player.get_state() != vlc.State.Playing:
            self.player.set_time(self.player.get_time())
        self._sync_slider()

    def pause_video(self):
        if not self._video_loaded:
            return
        self.player.pause()
        self.timer.stop()
        self._sync_slider()

    def stop_video(self):
        if not self._video_loaded:
            return
        self.player.stop()
        self.timer.stop()
        self.ui.timelineSlider.blockSignals(True)
        self.ui.timelineSlider.setRange(0, 1000)
        self.ui.timelineSlider.setValue(0)
        self.ui.timelineSlider.blockSignals(False)
        self.ui.lblCurrentTime.setText("00:00:00")
        self.ui.lblDuration.setText("00:00:00")

    def toggle_play_pause(self):
        if not self._video_loaded:
            return
        self.player.play_pause()
        if self.player.is_playing():
            self.timer.start()
        else:
            self.timer.stop()

    def next_frame(self):
        if not self._video_loaded:
            return
        self.player.next_frame()
        self.timer.stop()
        self._sync_slider()

    def previous_frame(self):
        if not self._video_loaded:
            return
        self.player.previous_frame()
        self.timer.stop()
        self._sync_slider()

    def _seek_relative(self, ms):
        if not self._video_loaded:
            return
        current = self.player.get_time()
        duration = self.player.get_length()
        new_time = max(0, min(duration, current + ms))
        self.player.set_time(new_time)
        self._sync_slider()

    def _go_to_start(self):
        if not self._video_loaded:
            return
        self.player.set_time(0)
        self._sync_slider()

    def _go_to_end(self):
        if not self._video_loaded:
            return
        duration = self.player.get_length()
        if duration > 0:
            self.player.set_time(duration - 1000)
            self._sync_slider()

    # ----------------------------------------------------------- speed
    def _on_speed_combo_changed(self, index):
        if index < 0 or index >= len(SPEEDS):
            return
        speed = SPEEDS[index]
        self.player.set_speed(speed)
        self._current_speed_index = index
        self.ui.statusbar.showMessage(f"Speed: {SPEED_LABELS[index]}", 2000)

    def _speed_up(self):
        if not self._video_loaded:
            return
        new_index = min(len(SPEEDS) - 1, self._current_speed_index + 1)
        self.ui.speedCombo.blockSignals(True)
        self.ui.speedCombo.setCurrentIndex(new_index)
        self.ui.speedCombo.blockSignals(False)
        self.player.set_speed(SPEEDS[new_index])
        self._current_speed_index = new_index
        self.ui.statusbar.showMessage(f"Speed: {SPEED_LABELS[new_index]}", 2000)

    def _speed_down(self):
        if not self._video_loaded:
            return
        new_index = max(0, self._current_speed_index - 1)
        self.ui.speedCombo.blockSignals(True)
        self.ui.speedCombo.setCurrentIndex(new_index)
        self.ui.speedCombo.blockSignals(False)
        self.player.set_speed(SPEEDS[new_index])
        self._current_speed_index = new_index
        self.ui.statusbar.showMessage(f"Speed: {SPEED_LABELS[new_index]}", 2000)

    # ----------------------------------------------------------- timer / sync
    def _on_timer_tick(self):
        state = self.player.get_state()
        if state in (vlc.State.Ended, vlc.State.Stopped):
            self.timer.stop()
            self.ui.timelineSlider.blockSignals(True)
            self.ui.timelineSlider.setValue(0)
            self.ui.timelineSlider.blockSignals(False)
            self.ui.lblCurrentTime.setText("00:00:00")
            return
        if self._slider_pressed:
            return
        self._sync_slider()

    def _sync_slider(self):
        current = self.player.get_time()
        duration = self.player.get_length()
        if duration > 0:
            self.ui.timelineSlider.blockSignals(True)
            self.ui.timelineSlider.setMaximum(duration)
            self.ui.timelineSlider.setValue(current)
            self.ui.timelineSlider.blockSignals(False)
        else:
            self.ui.timelineSlider.blockSignals(True)
            self.ui.timelineSlider.setRange(0, 1000)
            self.ui.timelineSlider.setValue(current)
            self.ui.timelineSlider.blockSignals(False)
        self.ui.lblCurrentTime.setText(self.format_time(current))
        self.ui.lblDuration.setText(self.format_time(duration))

    def _on_slider_moved(self, position):
        self.player.set_time(position)
        self.ui.lblCurrentTime.setText(self.format_time(position))
        self.ui.timelineSlider.blockSignals(True)
        self.ui.timelineSlider.setValue(position)
        self.ui.timelineSlider.blockSignals(False)

    def _on_slider_pressed(self):
        self._slider_pressed = True

    def _on_slider_released(self):
        pos = self.ui.timelineSlider.value()
        self.player.set_time(pos)
        self._sync_slider()
        self._slider_pressed = False

    def format_time(self, ms):
        seconds = max(0, int(ms // 1000))
        minutes = seconds // 60
        hours = minutes // 60
        return f"{hours:02}:{minutes % 60:02}:{seconds % 60:02}"

    # ----------------------------------------------------------- direction
    def on_direction_changed(self):
        if self.ui.rbIncoming.isChecked():
            self.counter.set_mode("Incoming")
        else:
            self.counter.set_mode("Outgoing")
        self.update_counter_table()

    # ----------------------------------------------------------- fullscreen
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

    # ----------------------------------------------------------- counter ops
    def undo_last(self):
        self.counter.undo()
        self.update_counter_table()

    def reset_counter(self):
        direction = self.counter.mode
        reply = QMessageBox.question(
            self,
            "Reset Counter",
            f"Are you sure you want to reset all {direction} counts?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.counter.reset_current()
            self.update_counter_table()

    # ----------------------------------------------------------- save / export
    def save_session(self):
        if not self.current_video:
            QMessageBox.warning(
                self, "Save Session", "Open a video first before saving a session."
            )
            return
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Session", "", "JSON Files (*.json)"
        )
        if not filename:
            return
        if not filename.lower().endswith(".json"):
            filename += ".json"
        session = CountingSession(
            video_path=self.current_video,
            incoming=self.counter.incoming.copy(),
            outgoing=self.counter.outgoing.copy(),
            notes="",
        )
        SessionService.save(session, filename)
        QMessageBox.information(self, "Save Session", f"Session saved to {filename}.")

    def export_counts(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Counts", "", "Excel Files (*.xlsx)"
        )
        if not filename:
            return
        if not filename.lower().endswith(".xlsx"):
            filename += ".xlsx"
        ExcelExporter.export(self.counter, filename)
        QMessageBox.information(self, "Export", f"Counts exported to {filename}.")

    def export_csv(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export CSV", "", "CSV Files (*.csv)"
        )
        if not filename:
            return
        if not filename.lower().endswith(".csv"):
            filename += ".csv"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Direction", "Vehicle", "Count", "Total"])
            for direction, counts in [
                ("Incoming", self.counter.incoming),
                ("Outgoing", self.counter.outgoing),
            ]:
                total = sum(counts.values())
                for vehicle in VEHICLE_CLASSES:
                    writer.writerow([
                        timestamp, direction, vehicle,
                        counts.get(vehicle, 0), total,
                    ])
        QMessageBox.information(self, "Export CSV", f"Counts exported to {filename}.")

    # ----------------------------------------------------------- about
    def show_about(self):
        QMessageBox.about(
            self,
            "About Vehicle Traffic Counter",
            "Vehicle Traffic Counter v1.0\n\n"
            "A professional desktop application for manual vehicle traffic counting.\n\n"
            "Powered by VLC and PyQt6.",
        )

    # ----------------------------------------------------------- key events
    def _handle_playback_shortcut(self, event):
        key = event.key()
        modifiers = event.modifiers()
        if key == Qt.Key.Key_Space:
            self.toggle_play_pause()
            return True
        if key == Qt.Key.Key_Left and modifiers & Qt.KeyboardModifier.ControlModifier:
            self._seek_relative(-5000)
            return True
        if key == Qt.Key.Key_Right and modifiers & Qt.KeyboardModifier.ControlModifier:
            self._seek_relative(5000)
            return True
        if key == Qt.Key.Key_Left:
            self.previous_frame()
            return True
        if key == Qt.Key.Key_Right:
            self.next_frame()
            return True
        if key == Qt.Key.Key_Home:
            self._go_to_start()
            return True
        if key == Qt.Key.Key_End:
            self._go_to_end()
            return True
        if key == Qt.Key.Key_Up:
            self._speed_up()
            return True
        if key == Qt.Key.Key_Down:
            self._speed_down()
            return True
        return False

    def _handle_counter_key(self, event):
        text = event.text().upper()
        if text in KEY_VEHICLE_MAP:
            vehicle = KEY_VEHICLE_MAP[text]
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                self.counter.decrement(vehicle)
            else:
                self.counter.increment(vehicle)
            self.update_counter_table()
            mode = self.counter.mode
            counts = self.counter.get_counts()
            op = "-1" if event.modifiers() & Qt.KeyboardModifier.ShiftModifier else "+1"
            self.ui.statusbar.showMessage(
                f"{mode}: {vehicle} {op} (Total: {sum(counts.values())})",
                3000,
            )
            return True
        return False

    def keyPressEvent(self, event):
        if self._handle_counter_key(event):
            return
        if self._handle_playback_shortcut(event):
            return
        super().keyPressEvent(event)

    def eventFilter(self, obj, event):
        if event.type() == event.Type.KeyPress:
            if self._handle_counter_key(event):
                return True
            if self._handle_playback_shortcut(event):
                return True
        return super().eventFilter(obj, event)
