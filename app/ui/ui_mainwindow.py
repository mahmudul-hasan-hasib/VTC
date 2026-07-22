from PyQt6 import QtCore, QtGui, QtWidgets


class ClickSlider(QtWidgets.QSlider):
    """QSlider subclass that jumps to click position instead of stepping."""

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            val = self.minimum() + (self.maximum() - self.minimum()) * event.position().x() / self.width()
            self.setValue(int(val))
            self.sliderMoved.emit(int(val))
        super().mousePressEvent(event)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        MainWindow.setMinimumSize(960, 600)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.centralLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.centralLayout.setSpacing(8)
        self.centralLayout.setContentsMargins(8, 8, 8, 8)
        self.centralLayout.setObjectName("centralLayout")

        # --- LEFT PANEL: Video (70%) ---
        self.videoPanelLayout = QtWidgets.QVBoxLayout()
        self.videoPanelLayout.setSpacing(4)
        self.videoPanelLayout.setContentsMargins(0, 0, 0, 0)
        self.videoPanelLayout.setObjectName("videoPanelLayout")

        self.videoFrame = QtWidgets.QFrame(parent=self.centralwidget)
        self.videoFrame.setMinimumSize(640, 400)
        self.videoFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.videoFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.videoFrame.setObjectName("videoFrame")
        self.videoPanelLayout.addWidget(self.videoFrame, 1)

        self.timelineSlider = ClickSlider(parent=self.centralwidget)
        self.timelineSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.timelineSlider.setObjectName("timelineSlider")
        self.timelineSlider.setEnabled(False)
        self.videoPanelLayout.addWidget(self.timelineSlider)

        self.timeLabelLayout = QtWidgets.QHBoxLayout()
        self.timeLabelLayout.setContentsMargins(0, 0, 0, 0)
        self.timeLabelLayout.setObjectName("timeLabelLayout")

        self.lblCurrentTime = QtWidgets.QLabel(parent=self.centralwidget)
        self.lblCurrentTime.setText("00:00:00")
        self.lblCurrentTime.setObjectName("lblCurrentTime")
        self.timeLabelLayout.addWidget(self.lblCurrentTime)

        spacer_time = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.timeLabelLayout.addItem(spacer_time)

        self.lblDuration = QtWidgets.QLabel(parent=self.centralwidget)
        self.lblDuration.setText("00:00:00")
        self.lblDuration.setObjectName("lblDuration")
        self.lblDuration.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.timeLabelLayout.addWidget(self.lblDuration)
        self.videoPanelLayout.addLayout(self.timeLabelLayout)

        self.transportLayout = QtWidgets.QHBoxLayout()
        self.transportLayout.setSpacing(4)
        self.transportLayout.setContentsMargins(0, 0, 0, 0)
        self.transportLayout.setObjectName("transportLayout")

        self.btnOpenVideo = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnOpenVideo.setText("Open Video")
        self.btnOpenVideo.setMinimumSize(90, 30)
        self.btnOpenVideo.setObjectName("btnOpenVideo")
        self.transportLayout.addWidget(self.btnOpenVideo)

        spacer_left = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.transportLayout.addItem(spacer_left)

        self.btnPrevFrame = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnPrevFrame.setText("\u25C0\u25C0")
        self.btnPrevFrame.setMinimumSize(38, 30)
        self.btnPrevFrame.setMaximumSize(38, 30)
        self.btnPrevFrame.setObjectName("btnPrevFrame")
        self.transportLayout.addWidget(self.btnPrevFrame)

        self.btnPlay = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnPlay.setText("\u25B6")
        self.btnPlay.setMinimumSize(38, 30)
        self.btnPlay.setMaximumSize(38, 30)
        self.btnPlay.setObjectName("btnPlay")
        self.transportLayout.addWidget(self.btnPlay)

        self.btnPause = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnPause.setText("\u23F8")
        self.btnPause.setMinimumSize(38, 30)
        self.btnPause.setMaximumSize(38, 30)
        self.btnPause.setObjectName("btnPause")
        self.transportLayout.addWidget(self.btnPause)

        self.btnStop = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnStop.setText("\u25A0")
        self.btnStop.setMinimumSize(38, 30)
        self.btnStop.setMaximumSize(38, 30)
        self.btnStop.setObjectName("btnStop")
        self.transportLayout.addWidget(self.btnStop)

        self.btnNextFrame = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnNextFrame.setText("\u25B6\u25B6")
        self.btnNextFrame.setMinimumSize(38, 30)
        self.btnNextFrame.setMaximumSize(38, 30)
        self.btnNextFrame.setObjectName("btnNextFrame")
        self.transportLayout.addWidget(self.btnNextFrame)

        spacer_mid = QtWidgets.QSpacerItem(12, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.transportLayout.addItem(spacer_mid)

        self.lblSpeed = QtWidgets.QLabel(parent=self.centralwidget)
        self.lblSpeed.setText("Speed:")
        self.lblSpeed.setObjectName("lblSpeed")
        self.transportLayout.addWidget(self.lblSpeed)

        self.speedCombo = QtWidgets.QComboBox(parent=self.centralwidget)
        self.speedCombo.setObjectName("speedCombo")
        self.speedCombo.setMinimumSize(65, 28)
        self.transportLayout.addWidget(self.speedCombo)

        spacer_right = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.transportLayout.addItem(spacer_right)
        self.videoPanelLayout.addLayout(self.transportLayout)

        self.centralLayout.addLayout(self.videoPanelLayout, 7)

        # --- RIGHT PANEL: Counter (30%) ---
        self.counterPanelLayout = QtWidgets.QVBoxLayout()
        self.counterPanelLayout.setSpacing(6)
        self.counterPanelLayout.setContentsMargins(0, 0, 0, 0)
        self.counterPanelLayout.setObjectName("counterPanelLayout")

        self.directionGroup = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.directionGroup.setTitle("Direction")
        self.directionGroup.setObjectName("directionGroup")
        self.directionLayout = QtWidgets.QHBoxLayout(self.directionGroup)
        self.directionLayout.setSpacing(12)
        self.directionLayout.setContentsMargins(8, 4, 8, 4)
        self.directionLayout.setObjectName("directionLayout")

        self.rbIncoming = QtWidgets.QRadioButton(parent=self.directionGroup)
        self.rbIncoming.setText("Incoming")
        self.rbIncoming.setChecked(True)
        self.rbIncoming.setObjectName("rbIncoming")
        self.directionLayout.addWidget(self.rbIncoming)

        self.rbOutgoing = QtWidgets.QRadioButton(parent=self.directionGroup)
        self.rbOutgoing.setText("Outgoing")
        self.rbOutgoing.setObjectName("rbOutgoing")
        self.directionLayout.addWidget(self.rbOutgoing)
        self.counterPanelLayout.addWidget(self.directionGroup)

        self.counterScrollArea = QtWidgets.QScrollArea(parent=self.centralwidget)
        self.counterScrollArea.setWidgetResizable(True)
        self.counterScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.counterScrollArea.setObjectName("counterScrollArea")
        self.counterWidget = QtWidgets.QWidget()
        self.counterWidget.setObjectName("counterWidget")
        self.counterScrollArea.setWidget(self.counterWidget)
        self.counterPanelLayout.addWidget(self.counterScrollArea, 1)

        self.actionLayout = QtWidgets.QHBoxLayout()
        self.actionLayout.setSpacing(6)
        self.actionLayout.setContentsMargins(0, 0, 0, 0)
        self.actionLayout.setObjectName("actionLayout")

        self.btnReset = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnReset.setText("Reset")
        self.btnReset.setObjectName("btnReset")
        self.actionLayout.addWidget(self.btnReset)

        self.btnExportReport = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnExportReport.setText("Export Excel Report")
        self.btnExportReport.setObjectName("btnExportReport")
        self.actionLayout.addWidget(self.btnExportReport)

        self.counterPanelLayout.addLayout(self.actionLayout)

        self.centralLayout.addLayout(self.counterPanelLayout, 3)

        MainWindow.setCentralWidget(self.centralwidget)

        # --- Menu Bar ---
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 30))
        self.menubar.setObjectName("menubar")

        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setTitle("File")
        self.menuFile.setObjectName("menuFile")
        self.menuPlayback = QtWidgets.QMenu(parent=self.menubar)
        self.menuPlayback.setTitle("Playback")
        self.menuPlayback.setObjectName("menuPlayback")
        self.menuHelp = QtWidgets.QMenu(parent=self.menubar)
        self.menuHelp.setTitle("Help")
        self.menuHelp.setObjectName("menuHelp")

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuPlayback.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # --- Actions ---
        self.actionOpen_Video = QtGui.QAction(parent=MainWindow)
        self.actionOpen_Video.setText("Open Video")
        self.actionOpen_Video.setShortcut("Ctrl+O")
        self.actionOpen_Video.setObjectName("actionOpen_Video")

        self.actionOpen_Folder = QtGui.QAction(parent=MainWindow)
        self.actionOpen_Folder.setText("Open Folder")
        self.actionOpen_Folder.setShortcut("Ctrl+F")
        self.actionOpen_Folder.setObjectName("actionOpen_Folder")

        self.actionExport_Report = QtGui.QAction(parent=MainWindow)
        self.actionExport_Report.setText("Export Excel Report")
        self.actionExport_Report.setShortcut("Ctrl+R")
        self.actionExport_Report.setObjectName("actionExport_Report")

        self.actionExit = QtGui.QAction(parent=MainWindow)
        self.actionExit.setText("Exit")
        self.actionExit.setShortcut("Ctrl+Q")
        self.actionExit.setObjectName("actionExit")

        self.actionPlay = QtGui.QAction(parent=MainWindow)
        self.actionPlay.setText("Play")
        self.actionPlay.setObjectName("actionPlay")

        self.actionPause = QtGui.QAction(parent=MainWindow)
        self.actionPause.setText("Pause")
        self.actionPause.setObjectName("actionPause")

        self.actionStop = QtGui.QAction(parent=MainWindow)
        self.actionStop.setText("Stop")
        self.actionStop.setObjectName("actionStop")

        self.actionPrevious_Frame = QtGui.QAction(parent=MainWindow)
        self.actionPrevious_Frame.setText("Previous Frame")
        self.actionPrevious_Frame.setShortcut("Left")
        self.actionPrevious_Frame.setObjectName("actionPrevious_Frame")

        self.actionNext_Frame = QtGui.QAction(parent=MainWindow)
        self.actionNext_Frame.setText("Next Frame")
        self.actionNext_Frame.setShortcut("Right")
        self.actionNext_Frame.setObjectName("actionNext_Frame")

        self.actionAbout = QtGui.QAction(parent=MainWindow)
        self.actionAbout.setText("About")
        self.actionAbout.setObjectName("actionAbout")

        self.actionKeyboard_Shortcuts = QtGui.QAction(parent=MainWindow)
        self.actionKeyboard_Shortcuts.setText("Keyboard Shortcuts")
        self.actionKeyboard_Shortcuts.setObjectName("actionKeyboard_Shortcuts")

        self.menuFile.addAction(self.actionOpen_Video)
        self.menuFile.addAction(self.actionOpen_Folder)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExport_Report)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)

        self.menuPlayback.addAction(self.actionPlay)
        self.menuPlayback.addAction(self.actionPause)
        self.menuPlayback.addAction(self.actionStop)
        self.menuPlayback.addSeparator()
        self.menuPlayback.addAction(self.actionPrevious_Frame)
        self.menuPlayback.addAction(self.actionNext_Frame)

        self.menuHelp.addAction(self.actionKeyboard_Shortcuts)
        self.menuHelp.addAction(self.actionAbout)
