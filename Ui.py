# -*- coding: utf-8 -*-
# @Author: hzb
# @Date:   2020-11-10 19:53:44
# @Last Modified by:   hzb
# @Last Modified time: 2020-12-25 18:21:26


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
    pre_rect = 0
    flag = False
    rects = []
    draw_cur = False
    draw_all = False
    draw_part = False
    delrect = []
    
    #鼠标点击事件
    def mousePressEvent(self,event):
        self.flag = True
        self.delrect = []
        self.x0 = event.x()
        self.y0 = event.y()
    #鼠标释放事件
    def mouseReleaseEvent(self,event):
        
        self.flag = False
        if self.x0 and self.y0:
            for rect in self.rects:
                if self.x0 > rect[0] and self.x0 < rect[2] and self.y0 > rect[1] and self.y0 < rect[3]:
                    self.delrect.append(rect)
            self.update()
        
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
        if self.draw_cur :
            painter.drawRect(self.rect) 
        elif self.draw_part:
            for rect in self.rects[self.pre_rect:]:
                box = QRect(rect[0], rect[1], abs(rect[2]-rect[0]), abs(rect[3]-rect[1]))
                painter.drawRect(box)
                painter.drawText(rect[0], rect[1]-3, rect[4]) 
        elif self.draw_all: 
            for rect in self.rects:
                # print('mark', rect)
                box = QRect(rect[0], rect[1], abs(rect[2]-rect[0]), abs(rect[3]-rect[1]))
                painter.drawRect(box)
                painter.drawText(rect[0], rect[1]-3, rect[4]) 
        if self.delrect:
            painter.setPen(QPen(Qt.green,2,Qt.SolidLine))
            for rect in self.delrect:
                box = QRect(rect[0], rect[1], abs(rect[2]-rect[0]), abs(rect[3]-rect[1]))
                painter.drawRect(box)
                self.x1 , self.y1 = self.x0, self.y0


        
    
    def append_rect(self, name):
        if self.rect:
            self.rects.append([self.x0, self.y0, self.x1, self.y1, name])
        self.x0, self.y0 = 0, 0
        self.x1, self.y1 = self.x0, self.y0
        # self.rect = QRect(self.x0, self.x0, self.x0, self.x0)
    def roi(self):
        roi = [self.x0, self.y0, self.x1, self.y1]
        self.x0, self.y0 = 0, 0
        self.x1, self.y1 = self.x0, self.y0
        return roi
    def del_rect(self):
        point = [self.x0, self.y0]
        self.x0, self.y0 = 0, 0
        self.x1 , self.y1 = self.x0, self.y0
        return point



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 960) 
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_clear = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_clear.setGeometry(QtCore.QRect(1130, 870, 130, 40))
        self.pushButton_clear.setFlat(False)
        self.pushButton_clear.setObjectName("pushButton_clear")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(170, 870, 130, 40))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setStyleSheet(
        '''QLineEdit{
                border:1px solid gray;
                width:300px;
                border-radius:10px;
                padding:2px 4px;
        }''')
        self.pushButton_add = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_add.setGeometry(QtCore.QRect(10, 870, 130, 40))
        self.pushButton_add.setObjectName("pushButton_add")
        self.pushButton_add.setShortcut('Ctrl+Z')
        self.pushButton_mark = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_mark.setGeometry(QtCore.QRect(490, 870, 130, 40))
        self.pushButton_mark.setObjectName("pushButton_mark")
        self.pushButton_start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start.setGeometry(QtCore.QRect(810, 870, 130, 40))
        self.pushButton_start.setObjectName("pushButton_start")
        self.horizontalScrollBar = QtWidgets.QScrollBar(self.centralwidget)
        self.horizontalScrollBar.setGeometry(QtCore.QRect(20, 840, 1171, 20))
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar.setObjectName("horizontalScrollBar")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(1190, 840, 100, 17))
        self.label.setObjectName("label")
        self.label_video = QtWidgets.QLabel(self.centralwidget)
        self.label_video.setGeometry(QtCore.QRect(1190, 15, 100, 20))
        self.label_video.setObjectName("label")
        self.lb = MyLabel(self) #重定义的label
        self.lb.setGeometry(QRect(41, 61, 1200, 800))
        self.lb.setObjectName("MyLabel")
        
        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(40, 20, 1200, 800))
        self.label2.setObjectName("label")
        self.label2.raise_()
        pe = QPalette()
        self.label2.setAutoFillBackground(True)#设置背景充满，为设置背景颜色的必要条件
        pe.setColor(QPalette.Window,Qt.white)#设置背景颜色
        self.label2.setPalette(pe)
        
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(650, 870, 130, 40))
        font = QtGui.QFont()
        font.setKerning(True)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.pushButton_roi = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_roi.setGeometry(QtCore.QRect(330, 870, 130, 40))
        self.pushButton_roi.setObjectName("pushButton_roi")
        self.pushButton_choose = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_choose.setGeometry(QtCore.QRect(970, 870, 130, 40))
        self.pushButton_choose.setObjectName("pushButton_choose")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 31))
        self.menubar.setObjectName("menubar")
        self.file = QtWidgets.QMenu(self.menubar)
        self.file.setObjectName("file")
        self.setting = QtWidgets.QStatusBar(self.menubar)
        self.setting.setObjectName("setting")
        self.setting_action = QtWidgets.QAction(self.setting)
        self.setting_action.setObjectName("setting_action")
        self.setting_action.setText("设置")

        self.manual = QtWidgets.QStatusBar(self.menubar)
        self.manual.setObjectName("manual")
        self.manual_action = QtWidgets.QAction(self.manual)
        self.manual_action.setObjectName("manual_action")
        self.manual_action.setText("使用说明")

        MainWindow.setMenuBar(self.menubar)
        self.open_video = QtWidgets.QAction(MainWindow)
        self.open_video.setObjectName("open_video")
        self.open_image = QtWidgets.QAction(MainWindow)
        self.open_image.setObjectName("open_image")
        
        self.open_client = QtWidgets.QAction(MainWindow)
        self.open_client.setObjectName("open_client")
        self.file.addAction(self.open_video)
        self.file.addAction(self.open_image)
        self.file.addAction(self.open_client)
        self.menubar.addAction(self.file.menuAction())
        self.menubar.addAction(self.setting_action)
        self.menubar.addAction(self.manual_action)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "光电情报处理系统"))
        self.pushButton_clear.setToolTip(_translate("MainWindow", "Ctrl+Del"))
        self.pushButton_clear.setText(_translate("MainWindow", "清空"))
        self.pushButton_clear.setShortcut(_translate("MainWindow", "Ctrl+Del"))
        self.pushButton_add.setToolTip(_translate("MainWindow", "Ctrl+S"))
        self.pushButton_add.setText(_translate("MainWindow", "框选"))
        self.pushButton_add.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.pushButton_mark.setToolTip(_translate("MainWindow", "Ctrl+D"))
        self.pushButton_mark.setText(_translate("MainWindow", "标注"))
        self.pushButton_mark.setShortcut(_translate("MainWindow", "Ctrl+D"))
        self.pushButton_start.setToolTip(_translate("MainWindow", "Ctrl+Space"))
        self.pushButton_start.setText(_translate("MainWindow", "开始"))
        self.pushButton_start.setShortcut(_translate("MainWindow", "Ctrl+Space"))
        self.label.setText(_translate("MainWindow", "--/--"))
        self.comboBox.setItemText(0, _translate("MainWindow", "      Siam"))
        self.comboBox.setItemText(1, _translate("MainWindow", "      KCF"))
        self.pushButton_roi.setToolTip(_translate("MainWindow", "Ctrl+F"))
        self.pushButton_roi.setText(_translate("MainWindow", "选区"))
        self.pushButton_roi.setShortcut(_translate("MainWindow", "Ctrl+F"))
        self.pushButton_choose.setToolTip(_translate("MainWindow", "Del"))
        self.pushButton_choose.setText(_translate("MainWindow", "删除目标"))
        self.pushButton_choose.setShortcut(_translate("MainWindow", "Del"))
        self.file.setTitle(_translate("MainWindow", "文件"))
        self.open_video.setText(_translate("MainWindow", "视频转换"))
        self.open_image.setText(_translate("MainWindow", "打开图片"))
        self.open_client.setText(_translate("MainWindow", "连接端口"))


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(547, 214)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(60, 58, 121, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(60, 128, 121, 31))
        self.label_2.setObjectName("label_2")
        self.pushButton_label = QtWidgets.QPushButton(Dialog)
        self.pushButton_label.setGeometry(QtCore.QRect(420, 60, 81, 29))
        self.pushButton_label.setObjectName("pushButton_label")
        self.lineEdit_label = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_label.setGeometry(QtCore.QRect(180, 60, 221, 29))
        self.lineEdit_label.setObjectName("lineEdit_label")
        self.lineEdit_UDP = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_UDP.setGeometry(QtCore.QRect(180, 130, 221, 29))
        self.lineEdit_UDP.setObjectName("lineEdit_UDP")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "设置"))
        self.label.setText(_translate("Dialog", "标签存储路径"))
        self.label_2.setText(_translate("Dialog", "服务器地址"))
        self.pushButton_label.setText(_translate("Dialog", "打开"))

class Ui_Dialog_manual(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(685, 515)
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(40, 30, 601, 451))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "使用说明"))
        self.textBrowser.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">使用说明：</p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">视频转换：自动切帧，并保存每帧图片</p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">打开图片：打开切帧后的图片文件夹</p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">连接端口：开始UDP传输，接收并保存图片</p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">设置：配置标签存储位置、UDP服务器地址</p>\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">框选：在界面上画框，可框选目标和跟踪区域</p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">输入框：输入目标类别名</p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">选取：确认跟踪区域</p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">标注：确认跟踪目标</p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Siam/KCF：选择跟踪算法</p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">开始/暂停：开始跟踪标注/暂停跟踪标注</p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">删除目标：鼠标点击目标，点击后删除</p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">清空：清空当前页面上所有目标</p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">滑条：显示跟踪进度、拖动可回看跟踪结果，可从任意位置开始</p>\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))


