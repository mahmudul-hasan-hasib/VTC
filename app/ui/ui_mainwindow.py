from PyQt6 import QtCore, QtGui, QtWidgets


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

        # --- LEFT PANEL: Video ---
        self.videoPanelLayout = QtWidgets.QVBoxLayout()
        self.videoPanelLayout.setSpacing(6)
        self.videoPanelLayout.setContentsMargins(0, 0, 0, 0)
        self.videoPanelLayout.setObjectName("videoPanelLayout")

        self.videoFrame = QtWidgets.QFrame(parent=self.centralwidget)
        self.videoFrame.setMinimumSize(480, 300)
        self.videoFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.videoFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.videoFrame.setObjectName("videoFrame")
        self.videoPanelLayout.addWidget(self.videoFrame)

        self.timelineSlider = QtWidgets.QSlider(parent=self.centralwidget)
        self.timelineSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.timelineSlider.setObjectName("timelineSlider")
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
        self.btnOpenVideo.setText("Open")
        self.btnOpenVideo.setMinimumSize(70, 32)
        self.btnOpenVideo.setObjectName("btnOpenVideo")
        self.transportLayout.addWidget(self.btnOpenVideo)

        spacer_left = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.transportLayout.addItem(spacer_left)

        self.btnPrevFrame = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnPrevFrame.setText("|<")
        self.btnPrevFrame.setMinimumSize(36, 32)
        self.btnPrevFrame.setMaximumSize(40, 32)
        self.btnPrevFrame.setObjectName("btnPrevFrame")
        self.transportLayout.addWidget(self.btnPrevFrame)

        self.btnPlay = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnPlay.setText(">")
        self.btnPlay.setMinimumSize(36, 32)
        self.btnPlay.setMaximumSize(40, 32)
        self.btnPlay.setObjectName("btnPlay")
        self.transportLayout.addWidget(self.btnPlay)

        self.btnPause = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnPause.setText("||")
        self.btnPause.setMinimumSize(36, 32)
        self.btnPause.setMaximumSize(40, 32)
        self.btnPause.setObjectName("btnPause")
        self.transportLayout.addWidget(self.btnPause)

        self.btnStop = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnStop.setText("#")
        self.btnStop.setMinimumSize(36, 32)
        self.btnStop.setMaximumSize(40, 32)
        self.btnStop.setObjectName("btnStop")
        self.transportLayout.addWidget(self.btnStop)

        self.btnNextFrame = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnNextFrame.setText(">|")
        self.btnNextFrame.setMinimumSize(36, 32)
        self.btnNextFrame.setMaximumSize(40, 32)
        self.btnNextFrame.setObjectName("btnNextFrame")
        self.transportLayout.addWidget(self.btnNextFrame)

        spacer_right = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.transportLayout.addItem(spacer_right)
        self.videoPanelLayout.addLayout(self.transportLayout)

        self.centralLayout.addLayout(self.videoPanelLayout, 3)

        # --- RIGHT PANEL: Counter ---
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

        self.tableWidget = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.tableWidget.setRowCount(2)
        self.tableWidget.setColumnCount(14)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setCornerButtonEnabled(False)
        self.tableWidget.setObjectName("tableWidget")
        self.counterPanelLayout.addWidget(self.tableWidget)

        self.actionLayout = QtWidgets.QHBoxLayout()
        self.actionLayout.setSpacing(6)
        self.actionLayout.setContentsMargins(0, 0, 0, 0)
        self.actionLayout.setObjectName("actionLayout")

        self.btnSave = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnSave.setText("Save Session")
        self.btnSave.setObjectName("btnSave")
        self.actionLayout.addWidget(self.btnSave)

        self.btnExport = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnExport.setText("Export CSV")
        self.btnExport.setObjectName("btnExport")
        self.actionLayout.addWidget(self.btnExport)

        self.btnReset = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnReset.setText("Reset")
        self.btnReset.setObjectName("btnReset")
        self.actionLayout.addWidget(self.btnReset)
        self.counterPanelLayout.addLayout(self.actionLayout)

        self.centralLayout.addLayout(self.counterPanelLayout, 2)

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

        self.actionExport_CSV = QtGui.QAction(parent=MainWindow)
        self.actionExport_CSV.setText("Export CSV")
        self.actionExport_CSV.setShortcut("Ctrl+E")
        self.actionExport_CSV.setObjectName("actionExport_CSV")

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
        self.actionPrevious_Frame.setObjectName("actionPrevious_Frame")

        self.actionNext_Frame = QtGui.QAction(parent=MainWindow)
        self.actionNext_Frame.setText("Next Frame")
        self.actionNext_Frame.setObjectName("actionNext_Frame")

        self.actionAbout = QtGui.QAction(parent=MainWindow)
        self.actionAbout.setText("About")
        self.actionAbout.setObjectName("actionAbout")

        self.menuFile.addAction(self.actionOpen_Video)
        self.menuFile.addAction(self.actionOpen_Folder)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExport_CSV)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)

        self.menuPlayback.addAction(self.actionPlay)
        self.menuPlayback.addAction(self.actionPause)
        self.menuPlayback.addAction(self.actionStop)
        self.menuPlayback.addSeparator()
        self.menuPlayback.addAction(self.actionPrevious_Frame)
        self.menuPlayback.addAction(self.actionNext_Frame)

        self.menuHelp.addAction(self.actionAbout)
