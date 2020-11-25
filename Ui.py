# -*- coding: utf-8 -*-
# @Author: hzb
# @Date:   2020-11-10 19:53:44
# @Last Modified by:   hzb
# @Last Modified time: 2020-11-25 16:36:26


# Form implementation generated from reading ui file '/media/jonthan/DATA/project/My_Classification/project.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QGuiApplication, QPalette
import cv2
import sys
   
class MyLabel(QLabel):
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = False
    rects = []
    draw_cur = False
    draw_all = False
    
    #鼠标点击事件
    def mousePressEvent(self,event):
        self.flag = True
        self.x0 = event.x()
        self.y0 = event.y()
    #鼠标释放事件
    def mouseReleaseEvent(self,event):
        self.flag = False
        
    #鼠标移动事件
    def mouseMoveEvent(self,event):
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()
    #绘制事件
    def paintEvent(self, event):
        super().paintEvent(event)
        self.rect = QRect(self.x0, self.y0, abs(self.x1-self.x0), abs(self.y1-self.y0))
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red,2,Qt.SolidLine))
        if self.draw_cur:
            painter.drawRect(self.rect)  
        elif self.draw_all: 
            for rect in self.rects:
                box = QRect(rect[0], rect[1], abs(rect[2]-rect[0]), abs(rect[3]-rect[1]))
                painter.drawRect(box)
    
    def append_rect(self, name):
        if self.rect:
            self.rects.append([self.x0, self.y0, self.x1, self.y1, name])
        self.rect = QRect(0, 0, 0, 0)



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 960)
        # self.setWindowOpacity(0.9) 
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_clear = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_clear.setGeometry(QtCore.QRect(720, 870, 120, 40))
        self.pushButton_clear.setFlat(False)
        self.pushButton_clear.setObjectName("pushButton_clear")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(150, 870, 120, 40))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setStyleSheet(
        '''QLineEdit{
                border:1px solid gray;
                width:300px;
                border-radius:10px;
                padding:2px 4px;
        }''')
        self.pushButton_add = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_add.setGeometry(QtCore.QRect(10, 870, 120, 40))
        self.pushButton_add.setObjectName("pushButton_add")
        self.pushButton_mark = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_mark.setGeometry(QtCore.QRect(290, 870, 120, 40))
        self.pushButton_mark.setObjectName("pushButton_mark")
        self.pushButton_start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start.setGeometry(QtCore.QRect(580, 870, 120, 40))
        self.pushButton_start.setObjectName("pushButton_start")
        self.horizontalScrollBar = QtWidgets.QScrollBar(self.centralwidget)
        self.horizontalScrollBar.setGeometry(QtCore.QRect(10, 840, 1171, 20))
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar.setObjectName("horizontalScrollBar")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(1190, 840, 100, 17))
        self.label.setObjectName("label")
        self.label_video = QtWidgets.QLabel(self.centralwidget)
        self.label_video.setGeometry(QtCore.QRect(1190, 15, 100, 20))
        self.label_video.setObjectName("label")
        self.lb = MyLabel(self) #重定义的label
        self.lb.setGeometry(QRect(40, 50, 1200, 800))
        self.lb.setObjectName("MyLabel")
        
        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(40, 20, 1200, 800))
        self.label2.setObjectName("label")
        self.label2.raise_()
        pe = QPalette()
        # pe.setColor(QPalette.WindowText,Qt.red)#设置字体颜色
        self.label2.setAutoFillBackground(True)#设置背景充满，为设置背景颜色的必要条件
        pe.setColor(QPalette.Window,Qt.white)#设置背景颜色
        self.label2.setPalette(pe)

        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setEnabled(True)
        self.checkBox.setGeometry(QtCore.QRect(440, 870, 120, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.checkBox.setFont(font)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.pushButton_det = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_det.setGeometry(QtCore.QRect(1000, 870, 120, 40))
        self.pushButton_det.setFlat(False)
        self.pushButton_det.setObjectName("pushButton_det")
        self.pushButton_train = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_train.setGeometry(QtCore.QRect(1140, 870, 120, 40))
        self.pushButton_train.setFlat(False)
        self.pushButton_train.setObjectName("pushButton_train")
        self.pushButton_change = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_change.setGeometry(QtCore.QRect(860, 870, 120, 40))
        self.pushButton_change.setFlat(False)
        self.pushButton_change.setObjectName("pushButton_change")
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
        MainWindow.setWindowTitle(_translate("MainWindow", "自动标注软件"))
        self.pushButton_clear.setText(_translate("MainWindow", "清除"))
        self.pushButton_add.setText(_translate("MainWindow", "添加目标"))
        self.pushButton_mark.setText(_translate("MainWindow", "标注"))
        self.pushButton_start.setText(_translate("MainWindow", "开始"))
        self.label.setText(_translate("MainWindow", "--/--"))
        # self.label_video.setText(_translate("MainWindow", "--/--"))
        self.checkBox.setText(_translate("MainWindow", "KCF / Siam"))
        self.pushButton_det.setText(_translate("MainWindow", "检测"))
        self.pushButton_train.setText(_translate("MainWindow", "训练"))
        self.pushButton_change.setText(_translate("MainWindow", "修改"))
        self.file.setTitle(_translate("MainWindow", "文件"))
        self.about.setTitle(_translate("MainWindow", "关于"))
        self.open_video.setText(_translate("MainWindow", "打开视频"))
        self.open_image.setText(_translate("MainWindow", "打开图片"))
        self.Manual.setText(_translate("MainWindow", "使用说明"))
        self.open_label.setText(_translate("MainWindow", "打开标签"))

