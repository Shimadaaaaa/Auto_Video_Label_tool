# -*- coding: utf-8 -*-
# @Author: hzb
# @Date:   2020-11-26 20:53:41
# @Last Modified by:   hzb
# @Last Modified time: 2020-12-01 13:33:13
import socket  
import threading  
import struct  
import os  
import time  
import sys
import numpy
import cv2
import re

class clientConnect:      
    def __init__(self, resolution = [1920,1080], remoteAddress = ("192.168.128.153", 
                    7999), windowName = "video"):          
        self.remoteAddress = remoteAddress        
        self.resolution = resolution          
        self.name = windowName          
        self.mutex = threading.Lock()        
        self.src=911+90        
        self.interval=0        
        self.path=os.getcwd()        
        self.img_quality = 90

        
    def _setSocket(self):      
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    def connect(self):     
        self._setSocket()
        self.socket.connect(self.remoteAddress) 
    def _processImage(self):    
        self.socket.send(struct.pack("lhh",self.src,self.resolution[0],self.resolution[1]))
        self.index = 0
        self.max_img = struct.unpack("i",self.socket.recv(12))[0] 
        # print(self.max_img)
        if not os.path.exists('./savePic'):
            os.mkdir('./savePic')
        while(1):        
            info = struct.unpack("lhh",self.socket.recv(12))        
            bufSize = info[0]        
            if bufSize:           
                 try:                  
                    self.mutex.acquire()                
                    self.buf=b''                
                    tempBuf=self.buf                
                    while(bufSize):                 #循环读取到一张图片的长度
                        tempBuf = self.socket.recv(bufSize)                    
                        bufSize -= len(tempBuf)                    
                        self.buf += tempBuf                
                        data = numpy.fromstring(self.buf,dtype='uint8')
                        self.image=cv2.imdecode(data,1)
                        self.index += 1
                        # print(self.index)
                        cv2.imwrite(f'./savePic/{self.index:06}.jpg', self.image)         
                        # cv2.imshow(self.name,self.image)            
                 except:                
                    #  print("接收失败")                
                     pass              
                 finally:                
                     self.mutex.release()               
                     if cv2.waitKey(10) == 27:                    
                         self.socket.close()                    
                         cv2.destroyAllWindows()                    
                         print("放弃连接")                    
                         break
            else:
                print('接收完成')
                return
                        
    def getData(self, interval):            
        showThread=threading.Thread(target=self._processImage) 
        showThread.setDaemon(True)    
        showThread.start()      
 

    def setWindowName(self, name):      
        self.name = name 
    def setRemoteAddress(remoteAddress):      
        self.remoteAddress = remoteAddress   


def main():    
    print("创建连接...")    
    cam = clientConnect()    
    # cam.check_config()    
    print("像素为:%d * %d"%(cam.resolution[0],cam.resolution[1]))    
    print("目标ip为%s:%d"%(cam.remoteAddress[0],cam.remoteAddress[1])) 
    cam.connect()      
    cam.getData(cam.interval) 
 
if __name__ == "__main__":      
    main()  