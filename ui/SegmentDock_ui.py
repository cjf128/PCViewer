# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SegmentDock.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
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
    QLabel, QListWidget, QListWidgetItem, QScrollArea,
    QSizePolicy, QSlider, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(222, 303)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(Form)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 218, 299))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.groupBox_3 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_15 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_15.setSpacing(2)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(2, 2, 2, 2)
        self.listWidget = QListWidget(self.groupBox_3)
        self.listWidget.setObjectName(u"listWidget")

        self.verticalLayout_15.addWidget(self.listWidget)


        self.verticalLayout_2.addWidget(self.groupBox_3)

        self.groupBox_2 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_14 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_14.setSpacing(2)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(2, 2, 2, 2)
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
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)

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


        self.verticalLayout_2.addWidget(self.groupBox_2)

        self.verticalSpacer = QSpacerItem(20, 150, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Form", u"\u6807\u6ce8\u9009\u62e9", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"\u6807\u6ce8\u8bbe\u7f6e", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u7b14\u5237\u5927\u5c0f", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"\u900f\u660e\u5ea6\uff1a  ", None))
    # retranslateUi

