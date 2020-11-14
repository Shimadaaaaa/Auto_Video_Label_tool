# -*- coding: utf-8 -*-
# @Author: hzb
# @Date:   2020-11-10 19:45:26
# @Last Modified by:   hzb
# @Last Modified time: 2020-11-13 20:39:20

import sys, cv2, time, os
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog,QTabWidget, QLabel,QWidget
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, Qt, QRect, QWaitCondition, QMutex, pyqtSignal, pyqtSlot, QCoreApplication
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QGuiApplication
from Ui import Ui_MainWindow
from redraw import redraw
from kcf import create_KCF, video_track, cut
from Siam import SiamRPN_load, siam_track
      

class mywindow(QMainWindow,Ui_MainWindow): #这个窗口继承了用QtDesignner 绘制的窗口

    def __init__(self):
        super(mywindow,self).__init__()
        self.setupUi(self)
        self.open_video.triggered.connect(self.videoprocessing)
        self.open_image.triggered.connect(self.imageprocessing)
        self.open_label.triggered.connect(self.labelprocessing)
        self.image_flag = False
        self.labelPath = './'
            
    def add_target(self):
        self.lb.draw_all = False
        self.lb.draw_cur = True
        

    def append_target(self):
        self.lb.draw_cur = False
        name = self.lineEdit.text()
        self.lb.append_rect(name)
        self.lb.draw_all = True
        self.lb.update()
        print(self.lb, self.lb.rects)

    def get_box(self, rects):
        res = []
        for rect in rects:
            box = []
            box.append(int((rect[0])/self.scale))
            box.append(int((rect[1]-(800 - self.height)/2)/self.scale) ) 
            box.append(int((rect[2])/self.scale))
            box.append(int((rect[3]-(800 - self.height)/2)/self.scale) )
            box.append(rect[4])
            res.append(box)
        return res       

    def labelprocessing(self):
        
        self.labelPath= QFileDialog.getExistingDirectory(None,
                                    "打开标签文件夹",
                                    "")
        print(self.labelPath)

    def videoprocessing(self):
        # print("gogo")

        videoName,videoType= QFileDialog.getOpenFileName(self, #返回路径下视频的全名称
                                    "打开视频",
                                    "",
                                    #" *.jpg;;*.png;;*.jpeg;;*.bmp")
                                    " *.avi;;*.mp4;;All Files (*)")
        print(videoType)
        img_path = str(videoName).replace('.'+str(videoType).split('.')[-1], '')
        print(img_path)
        if not os.path.exists(img_path):
            os.mkdir(img_path)
        self.label2.setPixmap(QPixmap(""))
        self.label2.setText('切割视频中')
        cut(str(videoName), img_path)
        self.label2.setText('切割完成')
        return

        
    
    def refreshShow(self):
        # 提取图像的尺寸和通道, 用于将opencv下的image转换成Qimage
        height, width, channel = self.img.shape
        bytesPerLine = 3 * width
        self.qImg = QImage(self.img.data, width, height, bytesPerLine,
                           QImage.Format_RGB888).rgbSwapped()
 
        # 将Qimage显示出来
        self.lb.setPixmap(QPixmap(""))
        self.lb.setCursor(Qt.CrossCursor)
        self.label2.setPixmap(QPixmap.fromImage(self.qImg))
        
        

    def setImage(self, image):
        self.label2.setPixmap(QPixmap.fromImage(image))
        self.label2.raise_()
    

    def imageprocessing(self):
        print('image')
        self.label2.setPixmap(QPixmap(""))
        self.imgPath= QFileDialog.getExistingDirectory(None,
                                    "打开图片文件夹",
                                    "")
        #利用qlabel显示图片
        print(str(self.imgPath))
        self.imgs = os.listdir(self.imgPath)
        self.imgs.sort()
        self.img = cv2.imread(os.path.join(self.imgPath, self.imgs[0]))
        self.scale = min(1200 / self.img.shape[1], 800 / self.img.shape[0])
        self.weight = int(self.scale*self.img.shape[1])
        self.height = int(self.scale * self.img.shape[0])
        self.img = cv2.resize(self.img, (self.weight, self.height))
        self.refreshShow()

        self.horizontalScrollBar.setValue(0)
        self.horizontalScrollBar.setMaximum(len(self.imgs)-1)

        self.lb.rects = []
        self.label.setText(str(self.horizontalScrollBar.value()) + '/' + str(len(self.imgs)-1))
        if self.image_flag : return
        self.image_flag = True

        self.pushButton_add.clicked.connect(self.add_target)
        self.pushButton_mark.clicked.connect(self.append_target)
        
        def playimage():
            self.th = Thread(self.imgPath, self.checkBox.isChecked())
            self.th.changePixmap.connect(self.setImage)
            self.th._curIndex = self.horizontalScrollBar.value()
            self.th.start()
            # print(self.checkBox.isChecked())
            self.boxes = self.get_box(self.lb.rects)
            self.th._curIndex = self.horizontalScrollBar.value()
            self.lb.draw_cur = False
            self.lb.draw_all = False
            # print(self.boxes)
            self.th.play(self.boxes, self.labelPath)
        def stopplay():
            self.th.pause()
            self.lb.rects = []
            self.horizontalScrollBar.setValue(self.th._curIndex+1)
            self.label.setText(str(self.horizontalScrollBar.value()) + '/' + str(len(self.imgs)-1))
        def jumpplay():
            self.label.setText(str(self.horizontalScrollBar.value()) + '/' + str(len(self.imgs)-1))
            self.img = cv2.imread(os.path.join(self.imgPath, self.imgs[self.horizontalScrollBar.value()]))
            txt_name = self.imgs[self.horizontalScrollBar.value()].replace('jpg', 'txt')
            txt = os.path.join(self.labelPath, txt_name)
            self.img = redraw(self.img, txt)
            self.img = cv2.resize(self.img, (self.weight, self.height))
            self.refreshShow()

        self.pushButton_start.clicked.connect(playimage)
        self.pushButton_stop.clicked.connect(stopplay)
        self.horizontalScrollBar.sliderMoved.connect(jumpplay)
              

class Thread(QThread):#采用线程来播放图片

    changePixmap = pyqtSignal(QtGui.QImage)

    def __init__(self, imgPath, iskcf):
        super().__init__()
        
        self.imgPath = imgPath
        self._isPause = True
        self._isFinish = False
        self._curIndex = 0
        self._boxes = []
        self.cond = QWaitCondition()
        self.mutex = QMutex()
        self.iskcf = iskcf
    
    def pause(self):
        self._isPause = True


    def play(self, boxes, txt_path):
        self._boxes = boxes
        self.txt_path = txt_path
        # print(self._boxes)
        self._isPause = False
        if self._isFinish == True:
            self._curIndex = 0
            self._isFinish = False
        self.cond.wakeAll()

    
    def jump(self, ind):
        self._curIndex = ind


    def run(self):
        imgs = os.listdir(self.imgPath)
        imgs.sort()
        self._mmax = len(imgs)
        img_path=os.path.join(self.imgPath,imgs[self._curIndex])
        first_img = cv2.imread(img_path)
        if self.iskcf:
            multiTracker, labels = create_KCF(first_img, self._boxes, self.txt_path)
        else :
            multiTracker, labels = SiamRPN_load(first_img, self._boxes, self.txt_path)
        # print('new', multiTracker)
        while(True):
            if self._curIndex >= self._mmax:
                self._isFinish = True
                self._isPause = True 
            self.mutex.lock()
            if self._isPause:self.cond.wait(self.mutex)
            img = imgs[self._curIndex]
            image = cv2.imread(os.path.join(self.imgPath, img))
            # print(self._boxes)
            if self.iskcf:
                multiTracker, image = video_track(image, img, self.txt_path, multiTracker, labels)
            else :
                multiTracker, image = siam_track(image, img, self.txt_path, multiTracker, labels)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            convertToQtFormat = QtGui.QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
            p = convertToQtFormat.scaled(1200, 800, Qt.KeepAspectRatio)
            self.changePixmap.emit(p)
            # time.sleep(0.01) #控制视频播放的速度
            self._curIndex += 1
            self.mutex.unlock() 


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = mywindow()
    window.show()
    sys.exit(app.exec_())
