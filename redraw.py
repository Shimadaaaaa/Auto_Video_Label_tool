# -*- coding: utf-8 -*-
# @Author: hzb
# @Date:   2020-11-12 00:08:25
# @Last Modified by:   hzb
# @Last Modified time: 2020-12-25 20:06:41
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

def reload(label_path, scale, height):
    res = []
    try:
        with open(label_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.replace('\n', '')
                box = line.split()
                box[:4] = list(map(int, box[:4]))
                box[:4] = [int(x * scale) for x in box[:4]]
                box[1] += (800 - height)/2
                box[3] += (800 - height)/2
                res.append(box)
                
        return res
    except:
        return res


    
if __name__ == "__main__": 
    img = redraw('/home/jonthan/下载/img/000001.jpg', '/home/jonthan/下载/txt/000001.txt')
    cv2.imshow('show', img)
    cv2.waitKey(0)