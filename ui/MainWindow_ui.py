# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDockWidget,
    QDoubleSpinBox, QFrame, QGroupBox, QHBoxLayout,
    QLabel, QMainWindow, QMenu, QMenuBar,
    QPushButton, QScrollArea, QScrollBar, QSizePolicy,
    QSlider, QSpacerItem, QSpinBox, QSplitter,
    QStackedWidget, QStatusBar, QToolBar, QVBoxLayout,
    QWidget)

from widgets.ImageViewer import ImageViewer
import designer_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1140, 789)
        MainWindow.setMinimumSize(QSize(0, 0))
        MainWindow.setAnimated(True)
        self.setting_atn = QAction(MainWindow)
        self.setting_atn.setObjectName(u"setting_atn")
        self.setting_atn.setCheckable(True)
        self.setting_atn.setChecked(True)
        icon = QIcon()
        if QIcon.hasThemeIcon(QIcon.ThemeIcon.DocumentProperties):
            icon = QIcon.fromTheme(QIcon.ThemeIcon.DocumentProperties)
        else:
            icon.addFile(u":/iocns/icons/setting_dark.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)

        self.setting_atn.setIcon(icon)
        self.load_atn = QAction(MainWindow)
        self.load_atn.setObjectName(u"load_atn")
        icon1 = QIcon()
        if QIcon.hasThemeIcon(QIcon.ThemeIcon.FolderOpen):
            icon1 = QIcon.fromTheme(QIcon.ThemeIcon.FolderOpen)
        else:
            icon1.addFile(u":/iocns/icons/openfile_dark.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)

        self.load_atn.setIcon(icon1)
        self.load_atn.setMenuRole(QAction.MenuRole.NoRole)
        self.load_atn.setIconVisibleInMenu(True)
        self.save_atn = QAction(MainWindow)
        self.save_atn.setObjectName(u"save_atn")
        icon2 = QIcon()
        if QIcon.hasThemeIcon(QIcon.ThemeIcon.DocumentSave):
            icon2 = QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave)
        else:
            icon2.addFile(u":/iocns/icons/save_dark.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)

        self.save_atn.setIcon(icon2)
        self.move_atn = QAction(MainWindow)
        self.move_atn.setObjectName(u"move_atn")
        self.move_atn.setCheckable(True)
        self.move_atn.setChecked(False)
        icon3 = QIcon()
        icon3.addFile(u":/iocns/icons/move.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.move_atn.setIcon(icon3)
        self.win_atn = QAction(MainWindow)
        self.win_atn.setObjectName(u"win_atn")
        self.win_atn.setCheckable(True)
        icon4 = QIcon()
        icon4.addFile(u":/iocns/icons/contrast.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.win_atn.setIcon(icon4)
        self.paint_atn = QAction(MainWindow)
        self.paint_atn.setObjectName(u"paint_atn")
        self.paint_atn.setCheckable(True)
        icon5 = QIcon()
        icon5.addFile(u":/iocns/icons/paint.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.paint_atn.setIcon(icon5)
        self.eraser_atn = QAction(MainWindow)
        self.eraser_atn.setObjectName(u"eraser_atn")
        self.eraser_atn.setCheckable(True)
        icon6 = QIcon()
        icon6.addFile(u":/iocns/icons/eraser.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.eraser_atn.setIcon(icon6)
        self.run_atn = QAction(MainWindow)
        self.run_atn.setObjectName(u"run_atn")
        icon7 = QIcon()
        icon7.addFile(u":/iocns/icons/run.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.run_atn.setIcon(icon7)
        self.actionexit = QAction(MainWindow)
        self.actionexit.setObjectName(u"actionexit")
        self.actionsave = QAction(MainWindow)
        self.actionsave.setObjectName(u"actionsave")
        self.actionopen = QAction(MainWindow)
        self.actionopen.setObjectName(u"actionopen")
        self.sam_atn = QAction(MainWindow)
        self.sam_atn.setObjectName(u"sam_atn")
        self.sam_atn.setCheckable(True)
        icon8 = QIcon()
        icon8.addFile(u":/iocns/icons/meta.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.sam_atn.setIcon(icon8)
        self.actionfile = QAction(MainWindow)
        self.actionfile.setObjectName(u"actionfile")
        self.actionfile.setCheckable(True)
        self.actionfile.setChecked(True)
        self.actionpaint = QAction(MainWindow)
        self.actionpaint.setObjectName(u"actionpaint")
        self.actionpaint.setCheckable(True)
        self.actionpaint.setChecked(True)
        self.actiontool = QAction(MainWindow)
        self.actiontool.setObjectName(u"actiontool")
        self.actiontool.setCheckable(True)
        self.actiontool.setChecked(True)
        self.actionrun = QAction(MainWindow)
        self.actionrun.setObjectName(u"actionrun")
        self.actionrun.setCheckable(True)
        self.actionrun.setChecked(True)
        self.aim_atn = QAction(MainWindow)
        self.aim_atn.setObjectName(u"aim_atn")
        self.aim_atn.setCheckable(True)
        self.aim_atn.setChecked(True)
        icon9 = QIcon()
        icon9.addFile(u":/iocns/icons/aim.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.aim_atn.setIcon(icon9)
        self.actioncrossline = QAction(MainWindow)
        self.actioncrossline.setObjectName(u"actioncrossline")
        self.actioncrossline.setCheckable(True)
        self.actioncrossline.setChecked(False)
        self.redo_atn = QAction(MainWindow)
        self.redo_atn.setObjectName(u"redo_atn")
        icon10 = QIcon()
        icon10.addFile(u":/iocns/icons/redo.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.redo_atn.setIcon(icon10)
        self.actionsegload = QAction(MainWindow)
        self.actionsegload.setObjectName(u"actionsegload")
        self.loadseg_atn = QAction(MainWindow)
        self.loadseg_atn.setObjectName(u"loadseg_atn")
        icon11 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.FolderNew))
        self.loadseg_atn.setIcon(icon11)
        self.loadseg_atn.setMenuRole(QAction.MenuRole.NoRole)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_5 = QFrame(self.centralwidget)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_5)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(self.frame_5)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.frame_2 = QFrame(self.splitter)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(600, 0))
        self.frame_2.setMaximumSize(QSize(16777215, 16777215))
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.frame_2)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 0))
        self.frame_3.setMaximumSize(QSize(16777215, 16777215))
        self.frame_3.setStyleSheet(u"")
        self.horizontalLayout_3 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(4, 4, 4, 4)
        self.boxPET = QCheckBox(self.frame_3)
        self.boxPET.setObjectName(u"boxPET")
        self.boxPET.setChecked(True)

        self.horizontalLayout_3.addWidget(self.boxPET)

        self.boxCT = QCheckBox(self.frame_3)
        self.boxCT.setObjectName(u"boxCT")
        self.boxCT.setChecked(True)

        self.horizontalLayout_3.addWidget(self.boxCT)

        self.boxSeg = QCheckBox(self.frame_3)
        self.boxSeg.setObjectName(u"boxSeg")
        self.boxSeg.setChecked(True)

        self.horizontalLayout_3.addWidget(self.boxSeg)

        self.sldLayer = QScrollBar(self.frame_3)
        self.sldLayer.setObjectName(u"sldLayer")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sldLayer.sizePolicy().hasHeightForWidth())
        self.sldLayer.setSizePolicy(sizePolicy)
        self.sldLayer.setMaximum(200)
        self.sldLayer.setValue(100)
        self.sldLayer.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_3.addWidget(self.sldLayer)

        self.boxLayer = QSpinBox(self.frame_3)
        self.boxLayer.setObjectName(u"boxLayer")
        self.boxLayer.setMaximum(1000)

        self.horizontalLayout_3.addWidget(self.boxLayer)

        self.btnCa = QPushButton(self.frame_3)
        self.btnCa.setObjectName(u"btnCa")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btnCa.sizePolicy().hasHeightForWidth())
        self.btnCa.setSizePolicy(sizePolicy1)
        self.btnCa.setMinimumSize(QSize(28, 28))
        self.btnCa.setMaximumSize(QSize(16777215, 16777215))
        self.btnCa.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.btnCa.setAutoRepeatDelay(300)

        self.horizontalLayout_3.addWidget(self.btnCa)


        self.verticalLayout_13.addWidget(self.frame_3)

        self.stackedWidget = QStackedWidget(self.frame_2)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_2 = QVBoxLayout(self.page)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.viewer = ImageViewer(self.page)
        self.viewer.setObjectName(u"viewer")
        self.viewer.setStyleSheet(u"background-color: rgb(0, 0, 0);")

        self.verticalLayout_2.addWidget(self.viewer)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_5 = QVBoxLayout(self.page_2)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.view_frame = QFrame(self.page_2)
        self.view_frame.setObjectName(u"view_frame")
        self.view_frame.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.view_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.view_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout_5.addWidget(self.view_frame)

        self.stackedWidget.addWidget(self.page_2)

        self.verticalLayout_13.addWidget(self.stackedWidget)

        self.frame_6 = QFrame(self.frame_2)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(30, 0))
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_7.setSpacing(6)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.btnH = QPushButton(self.frame_6)
        self.btnH.setObjectName(u"btnH")
        self.btnH.setMaximumSize(QSize(32, 32))
        self.btnH.setCheckable(True)
        self.btnH.setChecked(False)

        self.horizontalLayout_7.addWidget(self.btnH)

        self.btnS = QPushButton(self.frame_6)
        self.btnS.setObjectName(u"btnS")
        self.btnS.setMaximumSize(QSize(32, 32))
        self.btnS.setCheckable(True)

        self.horizontalLayout_7.addWidget(self.btnS)

        self.btnG = QPushButton(self.frame_6)
        self.btnG.setObjectName(u"btnG")
        self.btnG.setMaximumSize(QSize(32, 32))
        self.btnG.setCheckable(True)

        self.horizontalLayout_7.addWidget(self.btnG)

        self.btn3D = QPushButton(self.frame_6)
        self.btn3D.setObjectName(u"btn3D")
        self.btn3D.setMaximumSize(QSize(32, 32))
        self.btn3D.setCheckable(True)

        self.horizontalLayout_7.addWidget(self.btn3D)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer)

        self.btnReset = QPushButton(self.frame_6)
        self.btnReset.setObjectName(u"btnReset")
        icon12 = QIcon()
        icon12.addFile(u":/icons/icons/fix_light.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnReset.setIcon(icon12)

        self.horizontalLayout_7.addWidget(self.btnReset)


        self.verticalLayout_13.addWidget(self.frame_6)

        self.splitter.addWidget(self.frame_2)

        self.horizontalLayout.addWidget(self.splitter)


        self.verticalLayout.addWidget(self.frame_5)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 1140, 33))
        self.muFile = QMenu(self.menuBar)
        self.muFile.setObjectName(u"muFile")
        self.muView = QMenu(self.menuBar)
        self.muView.setObjectName(u"muView")
        MainWindow.setMenuBar(self.menuBar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        self.toolBar.setMinimumSize(QSize(32, 0))
        self.toolBar.setMovable(False)
        MainWindow.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.toolBar)
        self.toolBar_file = QToolBar(MainWindow)
        self.toolBar_file.setObjectName(u"toolBar_file")
        self.toolBar_file.setMinimumSize(QSize(0, 0))
        self.toolBar_file.setMovable(False)
        self.toolBar_file.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar_file)
        self.toolBar_draw = QToolBar(MainWindow)
        self.toolBar_draw.setObjectName(u"toolBar_draw")
        self.toolBar_draw.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar_draw)
        self.toolBar_run = QToolBar(MainWindow)
        self.toolBar_run.setObjectName(u"toolBar_run")
        self.toolBar_run.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar_run)
        self.dockWidget_2 = QDockWidget(MainWindow)
        self.dockWidget_2.setObjectName(u"dockWidget_2")
        self.dockWidget_2.setMinimumSize(QSize(230, 93))
        self.dockWidget_2.setFloating(False)
        self.dockWidgetContents_2 = QWidget()
        self.dockWidgetContents_2.setObjectName(u"dockWidgetContents_2")
        self.verticalLayout_4 = QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.scrollArea_2 = QScrollArea(self.dockWidgetContents_2)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 226, 675))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(2, 2, 2, 2)
        self.groupBox = QGroupBox(self.scrollAreaWidgetContents_2)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_10 = QVBoxLayout(self.groupBox)
        self.verticalLayout_10.setSpacing(2)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setSpacing(4)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(2, 2, 2, 2)
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_6.addWidget(self.label_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.sldAlphaPet = QSlider(self.groupBox)
        self.sldAlphaPet.setObjectName(u"sldAlphaPet")
        self.sldAlphaPet.setMaximum(100)
        self.sldAlphaPet.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_4.addWidget(self.sldAlphaPet)

        self.boxAlphaPet = QDoubleSpinBox(self.groupBox)
        self.boxAlphaPet.setObjectName(u"boxAlphaPet")
        self.boxAlphaPet.setMinimumSize(QSize(60, 0))
        self.boxAlphaPet.setMaximumSize(QSize(60, 16777215))
        self.boxAlphaPet.setMaximum(1.000000000000000)
        self.boxAlphaPet.setSingleStep(0.010000000000000)

        self.horizontalLayout_4.addWidget(self.boxAlphaPet)


        self.verticalLayout_6.addLayout(self.horizontalLayout_4)


        self.verticalLayout_10.addLayout(self.verticalLayout_6)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setSpacing(4)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(2, 2, 2, 2)
        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_8.addWidget(self.label_6)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.sldPET_ww = QSlider(self.groupBox)
        self.sldPET_ww.setObjectName(u"sldPET_ww")
        self.sldPET_ww.setMaximum(20000)
        self.sldPET_ww.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_5.addWidget(self.sldPET_ww)

        self.boxPET_ww = QDoubleSpinBox(self.groupBox)
        self.boxPET_ww.setObjectName(u"boxPET_ww")
        self.boxPET_ww.setMinimumSize(QSize(60, 0))
        self.boxPET_ww.setMaximumSize(QSize(60, 16777215))
        self.boxPET_ww.setMinimum(0.010000000000000)
        self.boxPET_ww.setMaximum(200.000000000000000)
        self.boxPET_ww.setSingleStep(0.010000000000000)

        self.horizontalLayout_5.addWidget(self.boxPET_ww)


        self.verticalLayout_8.addLayout(self.horizontalLayout_5)


        self.verticalLayout_10.addLayout(self.verticalLayout_8)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setSpacing(4)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(2, 2, 2, 2)
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_9.addWidget(self.label_4)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.sldPET_wl = QSlider(self.groupBox)
        self.sldPET_wl.setObjectName(u"sldPET_wl")
        self.sldPET_wl.setMaximum(10000)
        self.sldPET_wl.setValue(0)
        self.sldPET_wl.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_6.addWidget(self.sldPET_wl)

        self.boxPET_wl = QDoubleSpinBox(self.groupBox)
        self.boxPET_wl.setObjectName(u"boxPET_wl")
        self.boxPET_wl.setMinimumSize(QSize(60, 0))
        self.boxPET_wl.setMaximumSize(QSize(60, 16777215))
        self.boxPET_wl.setMinimum(0.010000000000000)
        self.boxPET_wl.setMaximum(100.000000000000000)
        self.boxPET_wl.setSingleStep(0.010000000000000)

        self.horizontalLayout_6.addWidget(self.boxPET_wl)


        self.verticalLayout_9.addLayout(self.horizontalLayout_6)


        self.verticalLayout_10.addLayout(self.verticalLayout_9)


        self.verticalLayout_3.addWidget(self.groupBox)

        self.line = QFrame(self.scrollAreaWidgetContents_2)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.line)

        self.groupBox_3 = QGroupBox(self.scrollAreaWidgetContents_2)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_16 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_16.setSpacing(2)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setSpacing(4)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(2, 2, 2, 2)
        self.label_3 = QLabel(self.groupBox_3)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_7.addWidget(self.label_3)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.sldAlphaCt = QSlider(self.groupBox_3)
        self.sldAlphaCt.setObjectName(u"sldAlphaCt")
        self.sldAlphaCt.setMaximum(100)
        self.sldAlphaCt.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_8.addWidget(self.sldAlphaCt)

        self.boxAlphaCt = QDoubleSpinBox(self.groupBox_3)
        self.boxAlphaCt.setObjectName(u"boxAlphaCt")
        self.boxAlphaCt.setMinimumSize(QSize(60, 0))
        self.boxAlphaCt.setMaximumSize(QSize(60, 16777215))
        self.boxAlphaCt.setMaximum(1.000000000000000)
        self.boxAlphaCt.setSingleStep(0.010000000000000)

        self.horizontalLayout_8.addWidget(self.boxAlphaCt)


        self.verticalLayout_7.addLayout(self.horizontalLayout_8)


        self.verticalLayout_16.addLayout(self.verticalLayout_7)

        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setSpacing(4)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(2, 2, 2, 2)
        self.label_8 = QLabel(self.groupBox_3)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_12.addWidget(self.label_8)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.sldCT_ww = QSlider(self.groupBox_3)
        self.sldCT_ww.setObjectName(u"sldCT_ww")
        self.sldCT_ww.setMaximum(3000)
        self.sldCT_ww.setValue(1)
        self.sldCT_ww.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_11.addWidget(self.sldCT_ww)

        self.boxCT_ww = QSpinBox(self.groupBox_3)
        self.boxCT_ww.setObjectName(u"boxCT_ww")
        self.boxCT_ww.setMinimumSize(QSize(60, 0))
        self.boxCT_ww.setMaximumSize(QSize(60, 16777215))
        self.boxCT_ww.setMinimum(1)
        self.boxCT_ww.setMaximum(3000)

        self.horizontalLayout_11.addWidget(self.boxCT_ww)


        self.verticalLayout_12.addLayout(self.horizontalLayout_11)


        self.verticalLayout_16.addLayout(self.verticalLayout_12)

        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setSpacing(4)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(2, 2, 2, 2)
        self.label_5 = QLabel(self.groupBox_3)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_11.addWidget(self.label_5)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.sldCT_wl = QSlider(self.groupBox_3)
        self.sldCT_wl.setObjectName(u"sldCT_wl")
        self.sldCT_wl.setMinimum(-2000)
        self.sldCT_wl.setMaximum(2000)
        self.sldCT_wl.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_10.addWidget(self.sldCT_wl)

        self.boxCT_wl = QSpinBox(self.groupBox_3)
        self.boxCT_wl.setObjectName(u"boxCT_wl")
        self.boxCT_wl.setMinimumSize(QSize(60, 0))
        self.boxCT_wl.setMaximumSize(QSize(60, 16777215))
        self.boxCT_wl.setMinimum(-2000)
        self.boxCT_wl.setMaximum(2000)

        self.horizontalLayout_10.addWidget(self.boxCT_wl)


        self.verticalLayout_11.addLayout(self.horizontalLayout_10)


        self.verticalLayout_16.addLayout(self.verticalLayout_11)


        self.verticalLayout_3.addWidget(self.groupBox_3)

        self.line_2 = QFrame(self.scrollAreaWidgetContents_2)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.line_2)

        self.groupBox_2 = QGroupBox(self.scrollAreaWidgetContents_2)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_14 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_14.setSpacing(2)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setSpacing(3)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.label_16 = QLabel(self.groupBox_2)
        self.label_16.setObjectName(u"label_16")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy2)
        self.label_16.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_19.addWidget(self.label_16)

        self.cboxMode = QComboBox(self.groupBox_2)
        self.cboxMode.addItem("")
        self.cboxMode.addItem("")
        self.cboxMode.setObjectName(u"cboxMode")

        self.horizontalLayout_19.addWidget(self.cboxMode)


        self.verticalLayout_14.addLayout(self.horizontalLayout_19)

        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")

        self.verticalLayout_14.addWidget(self.label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.sldPaint = QSlider(self.groupBox_2)
        self.sldPaint.setObjectName(u"sldPaint")
        self.sldPaint.setMinimum(1)
        self.sldPaint.setMaximum(30)
        self.sldPaint.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_2.addWidget(self.sldPaint)

        self.boxPaint = QSpinBox(self.groupBox_2)
        self.boxPaint.setObjectName(u"boxPaint")
        self.boxPaint.setMinimumSize(QSize(60, 0))
        self.boxPaint.setMaximumSize(QSize(60, 16777215))
        self.boxPaint.setMinimum(1)
        self.boxPaint.setMaximum(30)

        self.horizontalLayout_2.addWidget(self.boxPaint)


        self.verticalLayout_14.addLayout(self.horizontalLayout_2)

        self.label_9 = QLabel(self.groupBox_2)
        self.label_9.setObjectName(u"label_9")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy3)

        self.verticalLayout_14.addWidget(self.label_9)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.sldAlphaSeg = QSlider(self.groupBox_2)
        self.sldAlphaSeg.setObjectName(u"sldAlphaSeg")
        self.sldAlphaSeg.setMaximum(100)
        self.sldAlphaSeg.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_12.addWidget(self.sldAlphaSeg)

        self.boxAlphaSeg = QDoubleSpinBox(self.groupBox_2)
        self.boxAlphaSeg.setObjectName(u"boxAlphaSeg")
        self.boxAlphaSeg.setMinimumSize(QSize(60, 0))
        self.boxAlphaSeg.setMaximumSize(QSize(60, 16777215))
        self.boxAlphaSeg.setDecimals(2)
        self.boxAlphaSeg.setMaximum(1.000000000000000)
        self.boxAlphaSeg.setSingleStep(0.010000000000000)

        self.horizontalLayout_12.addWidget(self.boxAlphaSeg)


        self.verticalLayout_14.addLayout(self.horizontalLayout_12)


        self.verticalLayout_3.addWidget(self.groupBox_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.line_3 = QFrame(self.scrollAreaWidgetContents_2)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.line_3)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout_4.addWidget(self.scrollArea_2)

        self.dockWidget_2.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dockWidget_2)

        self.menuBar.addAction(self.muFile.menuAction())
        self.menuBar.addAction(self.muView.menuAction())
        self.muFile.addAction(self.actionopen)
        self.muFile.addAction(self.actionsegload)
        self.muFile.addAction(self.actionsave)
        self.muFile.addAction(self.actionexit)
        self.muView.addAction(self.actionfile)
        self.muView.addAction(self.actionpaint)
        self.muView.addAction(self.actiontool)
        self.muView.addAction(self.actionrun)
        self.muView.addAction(self.actioncrossline)
        self.toolBar.addAction(self.setting_atn)
        self.toolBar_file.addAction(self.load_atn)
        self.toolBar_file.addAction(self.loadseg_atn)
        self.toolBar_file.addAction(self.save_atn)
        self.toolBar_draw.addAction(self.aim_atn)
        self.toolBar_draw.addAction(self.move_atn)
        self.toolBar_draw.addAction(self.win_atn)
        self.toolBar_draw.addAction(self.paint_atn)
        self.toolBar_draw.addAction(self.eraser_atn)
        self.toolBar_draw.addAction(self.sam_atn)
        self.toolBar_run.addAction(self.run_atn)
        self.toolBar_run.addAction(self.redo_atn)

        self.retranslateUi(MainWindow)
        self.sldLayer.valueChanged.connect(self.boxLayer.setValue)
        self.boxLayer.valueChanged.connect(self.sldLayer.setValue)
        self.sldCT_ww.valueChanged.connect(self.boxCT_ww.setValue)
        self.boxCT_ww.valueChanged.connect(self.sldCT_ww.setValue)
        self.boxCT_wl.valueChanged.connect(self.sldCT_wl.setValue)
        self.sldCT_wl.valueChanged.connect(self.boxCT_wl.setValue)
        self.sldPaint.valueChanged.connect(self.boxPaint.setValue)
        self.boxPaint.valueChanged.connect(self.sldPaint.setValue)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.setting_atn.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
        self.load_atn.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u5165", None))
        self.save_atn.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58", None))
        self.move_atn.setText(QCoreApplication.translate("MainWindow", u"\u79fb\u52a8", None))
        self.win_atn.setText(QCoreApplication.translate("MainWindow", u"\u8c03\u7a97", None))
        self.paint_atn.setText(QCoreApplication.translate("MainWindow", u"\u6807\u6ce8", None))
        self.eraser_atn.setText(QCoreApplication.translate("MainWindow", u"\u64e6\u9664", None))
        self.run_atn.setText(QCoreApplication.translate("MainWindow", u"\u8fd0\u884c", None))
        self.actionexit.setText(QCoreApplication.translate("MainWindow", u"\u9000\u51fa", None))
        self.actionsave.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u4e3a", None))
        self.actionopen.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u6587\u4ef6\u5939", None))
        self.sam_atn.setText(QCoreApplication.translate("MainWindow", u"SAM", None))
        self.actionfile.setText(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6", None))
        self.actionpaint.setText(QCoreApplication.translate("MainWindow", u"\u56fe\u50cf", None))
        self.actiontool.setText(QCoreApplication.translate("MainWindow", u"\u4fa7\u680f", None))
        self.actionrun.setText(QCoreApplication.translate("MainWindow", u"\u8fd0\u884c", None))
        self.aim_atn.setText(QCoreApplication.translate("MainWindow", u"\u51c6\u5fc3", None))
        self.actioncrossline.setText(QCoreApplication.translate("MainWindow", u"\u5b9a\u4f4d\u7ebf", None))
        self.redo_atn.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u505a", None))
        self.actionsegload.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u5165\u6807\u6ce8", None))
        self.loadseg_atn.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u5165\u6807\u6ce8", None))
        self.boxPET.setText(QCoreApplication.translate("MainWindow", u"PET", None))
        self.boxCT.setText(QCoreApplication.translate("MainWindow", u"CT", None))
        self.boxSeg.setText(QCoreApplication.translate("MainWindow", u"Seg", None))
        self.btnCa.setText(QCoreApplication.translate("MainWindow", u"\u622a\u56fe", None))
        self.btnH.setText(QCoreApplication.translate("MainWindow", u"\u6a2a", None))
        self.btnS.setText(QCoreApplication.translate("MainWindow", u"\u77e2", None))
        self.btnG.setText(QCoreApplication.translate("MainWindow", u"\u51a0", None))
        self.btn3D.setText(QCoreApplication.translate("MainWindow", u"3D", None))
        self.btnReset.setText(QCoreApplication.translate("MainWindow", u"\u590d\u4f4d", None))
        self.muFile.setTitle(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6", None))
        self.muView.setTitle(QCoreApplication.translate("MainWindow", u"\u89c6\u56fe", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u4fa7\u680f", None))
        self.toolBar_file.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u4e3b\u5de5\u5177\u680f", None))
        self.toolBar_draw.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u5de5\u5177", None))
        self.toolBar_run.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u7a0b\u5e8f", None))
        self.dockWidget_2.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"PET", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u900f\u660e\u5ea6\uff1a  ", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u7a97\u5bbd\uff1a    ", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u7a97\u4f4d\uff1a    ", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"CT", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u900f\u660e\u5ea6\uff1a  ", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"\u7a97\u5bbd\uff1a    ", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u7a97\u4f4d\uff1a    ", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Segmentation", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"\u6807\u7b7e\u9009\u62e9\uff1a", None))
        self.cboxMode.setItemText(0, QCoreApplication.translate("MainWindow", u"\u539f\u53d1\u7076", None))
        self.cboxMode.setItemText(1, QCoreApplication.translate("MainWindow", u"\u8f6c\u79fb\u7076", None))

        self.label.setText(QCoreApplication.translate("MainWindow", u"\u7b14\u5237\u5927\u5c0f", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"\u900f\u660e\u5ea6\uff1a  ", None))
    # retranslateUi

