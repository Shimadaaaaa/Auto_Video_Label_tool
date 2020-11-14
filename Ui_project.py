# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/jonthan/DATA/project/My_Classification/auto_label_1_2/project.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 960)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_stop = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_stop.setGeometry(QtCore.QRect(1060, 870, 190, 40))
        self.pushButton_stop.setObjectName("pushButton_stop")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(230, 870, 190, 40))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_add = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_add.setGeometry(QtCore.QRect(10, 870, 190, 40))
        self.pushButton_add.setObjectName("pushButton_add")
        self.pushButton_mark = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_mark.setGeometry(QtCore.QRect(450, 870, 190, 40))
        self.pushButton_mark.setObjectName("pushButton_mark")
        self.pushButton_start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start.setGeometry(QtCore.QRect(840, 870, 190, 40))
        self.pushButton_start.setObjectName("pushButton_start")
        self.horizontalScrollBar = QtWidgets.QScrollBar(self.centralwidget)
        self.horizontalScrollBar.setGeometry(QtCore.QRect(20, 840, 1171, 20))
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar.setObjectName("horizontalScrollBar")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(1210, 840, 67, 17))
        self.label.setObjectName("label")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setEnabled(True)
        self.checkBox.setGeometry(QtCore.QRect(680, 870, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.checkBox.setFont(font)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 31))
        self.menubar.setObjectName("menubar")
        self.file = QtWidgets.QMenu(self.menubar)
        self.file.setObjectName("file")
        self.about = QtWidgets.QMenu(self.menubar)
        self.about.setObjectName("about")
        MainWindow.setMenuBar(self.menubar)
        self.open_video = QtWidgets.QAction(MainWindow)
        self.open_video.setObjectName("open_video")
        self.open_image = QtWidgets.QAction(MainWindow)
        self.open_image.setObjectName("open_image")
        self.Manual = QtWidgets.QAction(MainWindow)
        self.Manual.setObjectName("Manual")
        self.open_label = QtWidgets.QAction(MainWindow)
        self.open_label.setObjectName("open_label")
        self.file.addAction(self.open_video)
        self.file.addAction(self.open_image)
        self.file.addAction(self.open_label)
        self.about.addAction(self.Manual)
        self.menubar.addAction(self.file.menuAction())
        self.menubar.addAction(self.about.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_stop.setText(_translate("MainWindow", "暂停"))
        self.pushButton_add.setText(_translate("MainWindow", "添加目标"))
        self.pushButton_mark.setText(_translate("MainWindow", "标注"))
        self.pushButton_start.setText(_translate("MainWindow", "开始"))
        self.label.setText(_translate("MainWindow", "1/100"))
        self.checkBox.setText(_translate("MainWindow", "KCF / Siam"))
        self.file.setTitle(_translate("MainWindow", "文件"))
        self.about.setTitle(_translate("MainWindow", "关于"))
        self.open_video.setText(_translate("MainWindow", "打开视频"))
        self.open_image.setText(_translate("MainWindow", "打开图片"))
        self.Manual.setText(_translate("MainWindow", "使用说明"))
        self.open_label.setText(_translate("MainWindow", "打开标签"))

