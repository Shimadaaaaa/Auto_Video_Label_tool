# -*- coding: utf-8 -*-
# @Author: hzb
# @Date:   2020-11-10 19:45:26
# @Last Modified by:   hzb
# @Last Modified time: 2020-11-25 16:46:21

import sys, cv2, time, os
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog,QTabWidget, QLabel,QWidget
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, Qt, QRect, QWaitCondition, QMutex, pyqtSignal, pyqtSlot, QCoreApplication
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QGuiApplication
from Ui import Ui_MainWindow
from redraw import redraw, Manual
from kcf import create_KCF, video_track
from Siam import SiamRPN_load, siam_track
import style_rc


class mywindow(QMainWindow,Ui_MainWindow): 
    def __init__(self):
        super(mywindow,self).__init__()
        self.setupUi(self)
        self.open_video.triggered.connect(self.videoprocessing)
        self.open_image.triggered.connect(self.imageprocessing)
        self.open_label.triggered.connect(self.labelprocessing)
        self.Manual.triggered.connect(self.show_manual)
        self.image_flag = False
        self.max_img = 0
        self.labelPath = './'

    def show_manual(self):
        #显示使用说明
        self.label2.setPixmap(QPixmap(""))
        self.label2.setText(Manual)

    def add_target(self):
        #修改画框事件中的两个flag值
        #框选新目标
        self.lb.draw_all = False
        self.lb.draw_cur = True
        

    def append_target(self):
        #确定添加目标
        self.lb.draw_cur = False
        name = self.lineEdit.text()
        self.lb.append_rect(name)
        self.lb.draw_all = True
        self.lb.update()
        print(self.lb, self.lb.rects)

    def get_box(self, rects):
        #将qt画的框按比例还原到原图尺寸
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
        #打开标签所在路径
        self.labelPath= QFileDialog.getExistingDirectory(None,
                                    "打开标签文件夹",
                                    "")
        if not self.labelPath: return
        print(self.labelPath)

    def videoprocessing(self):
        #打开视频进行切帧，存储在视频路径下视频同名文件夹内
        self.label_video.setText('')
        videoName,videoType= QFileDialog.getOpenFileName(self, #返回路径下视频的全名称
                                    "打开视频",
                                    "",
                                    #" *.jpg;;*.png;;*.jpeg;;*.bmp")
                                    " *.MP4;;*.mp4;;*.avi;;All Files (*)")
        #未打开视频直接返回
        if not videoName: return
        img_path = str(videoName).replace('.'+str(videoType).split('.')[-1], '')
        vc = cv2.VideoCapture(videoName)
        #获得视频总帧数
        self.max_img = int(vc.get(cv2.CAP_PROP_FRAME_COUNT))
        #构造线程进行切帧
        self.th2 = Cut(videoName, img_path)
        self.th2.start()
        def show_progress():
            if self.th2.n == self.max_img:
                #当切到最后一帧，将max_img归零
                self.max_img = 0
                self.label_video.setText('切帧完成')
            else:
                #更新显示当前切帧进度
                self.label_video.setText(str(self.th2.n-1) + '/' + str(self.max_img-1))
        #将线程内的index更新信号与显示函数绑定
        self.th2.cutOut.connect(show_progress)
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
        #跟踪时更新画面调用的显示函数
        self.label2.setPixmap(QPixmap.fromImage(image))
        self.label2.raise_()
    

    def imageprocessing(self):
        #打开图片文件夹，激活相关功能按键
        _translate = QCoreApplication.translate
        print('image')
        #清除上次切帧完成的字
        self.label2.setPixmap(QPixmap(""))
        self.imgPath= QFileDialog.getExistingDirectory(None,
                                    "打开图片文件夹",
                                    "")
        if not self.imgPath: return 
        print(str(self.imgPath))
        #显示第一帧
        self.imgs = os.listdir(self.imgPath)
        self.imgs.sort()
        self.img = cv2.imread(os.path.join(self.imgPath, self.imgs[0]))
        #计算等比例缩放的比例
        self.scale = min(1200 / self.img.shape[1], 800 / self.img.shape[0])
        self.weight = int(self.scale*self.img.shape[1])
        self.height = int(self.scale * self.img.shape[0])
        self.img = cv2.resize(self.img, (self.weight, self.height))
        self.refreshShow()
        #设定滑条初始位置为0
        self.horizontalScrollBar.setValue(0)
        if self.max_img:
            #依靠max_img判断是否是切帧状态，如果是，设定滑条长度为总帧数-1
            self.horizontalScrollBar.setMaximum(self.max_img-1)
        else:
            #如果不是，则是普通图片状态，设定滑条长度为总图片数-1
            self.horizontalScrollBar.setMaximum(len(self.imgs)-1)
            
        #将画框事件中的框清空
        self.lb.rects = []
        #设置进度显示
        if self.max_img:
            self.label.setText(str(self.horizontalScrollBar.value()) + '/' + str(self.max_img-1))
        else:
            self.label.setText(str(self.horizontalScrollBar.value()) + '/' + str(len(self.imgs)-1))
        #判断是否是第一次开启，如果不是则修改完参数返回，否则会出现同时多个imageprocessing进程在执行
        if self.image_flag : return
        self.image_flag = True
        #添加目标按键和标注按键绑定功能
        self.pushButton_add.clicked.connect(self.add_target)
        self.pushButton_mark.clicked.connect(self.append_target)
        def movebar():
            #随着跟踪进度移动滑条
            self.horizontalScrollBar.setValue(self.th._curIndex-1)
            if self.max_img:
                self.label.setText(str(self.horizontalScrollBar.value()) + '/' + str(self.max_img-1))
            else:
                self.label.setText(str(self.horizontalScrollBar.value()) + '/' + str(len(self.imgs)-1))
        def playimage():
            #跟踪开始
            #构建跟踪进程
            self.th = Thread(self.imgPath, self.checkBox.isChecked())
            self.th.changePixmap.connect(self.setImage)
            self.th.sinOut.connect(movebar)
            #从滑条获取起始index
            self.th._curIndex = self.horizontalScrollBar.value()
            self.th.start()
            # print(self.checkBox.isChecked())
            self.boxes = self.get_box(self.lb.rects)
            self.th._curIndex = self.horizontalScrollBar.value()
            self.lb.draw_cur = False
            self.lb.draw_all = False
            # print(self.boxes)
            self.th.play(self.boxes, self.labelPath)
            #开始后将开始键变成暂停键
            self.pushButton_start.setText(_translate("MainWindow", "暂停"))
            #去除开始功能
            self.pushButton_start.disconnect()
            #绑定暂停功能
            self.pushButton_start.clicked.connect(stopplay)
            #跟踪时禁用拖动滑条功能
            self.horizontalScrollBar.disconnect()
        def stopplay():
            #暂停功能
            self.th.pause()
            #清空之前的所有框
            self.lb.rects = []
            self.pushButton_start.setText(_translate("MainWindow", "开始"))
            #去除暂停功能
            self.pushButton_start.disconnect()
            #绑定开始功能
            self.pushButton_start.clicked.connect(playimage)
            #暂停时开启拖动滑条速度
            self.horizontalScrollBar.valueChanged.connect(jumpplay)
            self.horizontalScrollBar.sliderMoved.connect(jumpplay)
        def jumpplay():
            #滑动功能
            if self.max_img:
                #如果在切帧，重新加载图片列表
                self.imgs = os.listdir(self.imgPath)
                self.imgs.sort()
                self.label.setText(str(self.horizontalScrollBar.value()) + '/' + str(self.max_img-1))
            else:
                self.label.setText(str(self.horizontalScrollBar.value()) + '/' + str(len(self.imgs)-1))
            self.img = cv2.imread(os.path.join(self.imgPath, self.imgs[self.horizontalScrollBar.value()]))
            #依照txt内容重绘之前跟踪结果
            txt_name = self.imgs[self.horizontalScrollBar.value()].replace('jpg', 'txt')
            txt = os.path.join(self.labelPath, txt_name)
            self.img = redraw(self.img, txt)
            self.img = cv2.resize(self.img, (self.weight, self.height))
            self.refreshShow()
        def clearrect():
            #清空功能，重新显示当前帧的原始图片
            self.img = cv2.imread(os.path.join(self.imgPath, self.imgs[self.horizontalScrollBar.value()]))
            self.img = cv2.resize(self.img, (self.weight, self.height))
            self.refreshShow()
        self.pushButton_start.clicked.connect(playimage)
        self.pushButton_clear.clicked.connect(clearrect)
        self.horizontalScrollBar.sliderMoved.connect(jumpplay)
        self.horizontalScrollBar.valueChanged.connect(jumpplay)
        

class Thread(QThread): #采用线程来跟踪、显示
    #图片更新
    changePixmap = pyqtSignal(QtGui.QImage)
    #进度信号
    sinOut = pyqtSignal(int)

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
            imgs = os.listdir(self.imgPath)
            imgs.sort()
            self._mmax = len(imgs)
            if self._curIndex >= self._mmax:
                self._isFinish = True
                self._isPause = True 
            self.mutex.lock()
            if self._isPause:self.cond.wait(self.mutex)
            img = imgs[self._curIndex]
            image = cv2.imread(os.path.join(self.imgPath, img))
            # print(self._boxes)
            #选择跟踪算法
            if self.iskcf:
                multiTracker, image = video_track(image, img, self.txt_path, multiTracker, labels)
            else :
                multiTracker, image = siam_track(image, img, self.txt_path, multiTracker, labels)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            convertToQtFormat = QtGui.QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
            p = convertToQtFormat.scaled(1200, 800, Qt.KeepAspectRatio)
            self.changePixmap.emit(p)
            self.sinOut.emit(self._curIndex)
            self._curIndex += 1
            self.mutex.unlock() 

class Cut(QThread): #切帧线程
    #切帧进度信号
    cutOut = pyqtSignal(int)
    def __init__(self, video_in, img_out):
        super().__init__()
        self.video_in = video_in
        self.img_out = img_out
        self.n = 0
        if not os.path.exists(img_out):
            os.makedirs(img_out)

    def run(self):
        #读图存图
        cap = cv2.VideoCapture(self.video_in)
        while True:
            _,frame=cap.read()
            if _:
                self.cutOut.emit(self.n)
                self.n += 1
                id = '%06d' % self.n
                img_name = str(id)+'.jpg'
                cv2.imwrite(os.path.join(self.img_out,img_name),frame)
            else:break
        cap.release()
        return  


if __name__ == '__main__':
    app = QApplication(sys.argv)
    #加载风格模板
    with open("darkstyle.qss") as f:
        stylesheet = f.read()
    app.setStyleSheet(stylesheet)
    window = mywindow()
    window.show()
    sys.exit(app.exec_())
