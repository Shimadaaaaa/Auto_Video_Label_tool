# -*- coding: utf-8 -*-
# @Author: hzb
# @Date:   2020-11-12 00:08:25
# @Last Modified by:   hzb
# @Last Modified time: 2020-11-25 16:47:37
import os
import cv2
import numpy as np

def redraw(img, label_path):
    try:
        with open(label_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.replace('\n', '')
                box = line.split()
                box[:4] = list(map(int, box[:4]))
                img = cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (0, 0, 255), 2)
                img = cv2.putText(img, box[4], (box[0], box[1]-3),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        return img
    except:
        return img

Manual = '打开视频：自动切帧\n打开图片：打开切帧后的图片文件夹\n打开标签：打开标注文件保存文件夹\n添加目标：左侧输入类别名称，鼠标画框\n标注：确认添加标记框\nKCF/Siam：选择跟踪使用的算法\n开始：开始自动标注\n暂停：结束标注\n滑条：拖动回看标注结果，并可以从任意位置重新标记后重新标注\n清空：清空画面全有标注\n'  
    
if __name__ == "__main__": 
    img = redraw('/home/jonthan/下载/img/000001.jpg', '/home/jonthan/下载/txt/000001.txt')
    cv2.imshow('show', img)
    cv2.waitKey(0)