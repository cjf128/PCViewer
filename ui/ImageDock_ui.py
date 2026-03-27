# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ImageDock.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QGroupBox, QHBoxLayout,
    QLabel, QScrollArea, QSizePolicy, QSlider,
    QSpacerItem, QSpinBox, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(246, 558)
        self.verticalLayout_3 = QVBoxLayout(Form)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(Form)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 244, 556))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.groupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
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


        self.verticalLayout.addLayout(self.verticalLayout_6)

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


        self.verticalLayout.addLayout(self.verticalLayout_8)

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


        self.verticalLayout.addLayout(self.verticalLayout_9)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.groupBox_3 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_16 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_16.setSpacing(0)
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


        self.verticalLayout_2.addWidget(self.groupBox_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_3.addWidget(self.scrollArea)


        self.retranslateUi(Form)
        self.boxCT_ww.valueChanged.connect(self.sldCT_ww.setValue)
        self.sldCT_ww.valueChanged.connect(self.boxCT_ww.setValue)
        self.boxCT_wl.valueChanged.connect(self.sldCT_wl.setValue)
        self.sldCT_wl.valueChanged.connect(self.boxCT_wl.setValue)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"PET", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u900f\u660e\u5ea6\uff1a  ", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"\u7a97\u5bbd\uff1a    ", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u7a97\u4f4d\uff1a    ", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Form", u"CT", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u900f\u660e\u5ea6\uff1a  ", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"\u7a97\u5bbd\uff1a    ", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u7a97\u4f4d\uff1a    ", None))
    # retranslateUi

