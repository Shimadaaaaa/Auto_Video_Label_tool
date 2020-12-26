# -*- coding: utf-8 -*-
# @Author: hzb
# @Date:   2020-11-12 16:58:13
# @Last Modified by:   hzb
# @Last Modified time: 2020-12-24 21:57:18
#多目标视频追踪
#框选感兴趣的矩形区域后，回车两下，进行下一目标的框选。若目标全部框选完毕，按回车后再按q退出，开始跟踪。
import sys
import cv2
from random import randint
import time
import os
# import av
import numpy as np

def create_KCF(image,bboxes,txt_path):
    if not os.path.exists(txt_path):
        os.makedirs(txt_path)
    multiTracker = cv2.MultiTracker_create()
    #tracker = cv2.TrackerKCF_create()
    labels=[]
    # print(bboxes)
    for bbox in bboxes:
        tracker = cv2.TrackerKCF_create()
        labels.append(bbox[-1])
        #print(np.array(bbox[2:4]))
        #bbox[0:2],bbox[2:4]=np.array(bbox[2:4])+np.array(bbox[0:2])//2,np.array(bbox[2:4])-np.array(bbox[0:2])
        bbox[2:4]=np.array(bbox[2:4])-np.array(bbox[0:2])
        # print(bbox,'----')
        multiTracker.add(tracker, image, tuple(bbox[:4])) 
    return multiTracker,labels

def video_track(image,img_name,txt_path,multiTracker,labels): 
    ret, bboxes = multiTracker.update(image)
    mess=''
    for i, newbox in enumerate(bboxes):
        # print(newbox)
        p1 = (int(newbox[0]), int(newbox[1]))
        p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
        cv2.rectangle(image, p1, p2, (0,0,255), 2, 1)
        cv2.putText(image, labels[i], (p1[0], p1[1]-3),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        mess+=f'{(p1[0])} {p1[1]} {p2[0]} {p2[1]} {labels[i]} \n'
    txt_name = img_name.replace('.jpg','.txt')
    # print(img_name, txt_name)
    txt_path_out=os.path.join(txt_path,txt_name)
    file_handle=open(txt_path_out,mode='w')
    file_handle.write(mess)
    file_handle.close()
    return multiTracker,image

def cut(video_in,img_out):
    if not os.path.exists(img_out):
        os.makedirs(img_out)
    n=0
    cap = cv2.VideoCapture(video_in)
    while True:
        _,frame=cap.read()
        if _:
            n = n+1
            id='%06d'%n
            img_name = str(id)+'.jpg'
            cv2.imwrite(os.path.join(img_out,img_name),frame)
        else:break
    cap.release() 


if __name__ == '__main__':
    # txt_path =  '/home/jonthan/下载/txt/'
    # img_path= '/home/jonthan/下载/img/'
    # image_list=os.listdir(img_path)
    # image_list.sort()
    # image=cv2.imread(img_path+image_list[0])
    # bboxes=[[539,194,640,289,'1'],[600,600,800,800,'2']]
    # multiTracker,labels=create_KCF(image,bboxes,txt_path)
    # for i in image_list:
    #     image=cv2.imread(img_path+i)
    #     multiTracker,image=video_track(image,i,txt_path,multiTracker,labels)
    #     cv2.imshow('img',image)
    #     cv2.waitKey(1)
    #     time.sleep(1)
    t_s = time.time()
    video_path = '/media/jonthan/Jonthan/video/20201002123733.MP4'
    image_path = '/media/jonthan/Jonthan/video/20201002123733'
    cut(video_path, image_path)
    # print(time.time() - t_s)