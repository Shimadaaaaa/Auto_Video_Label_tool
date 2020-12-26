# -*- coding: utf-8 -*-
# @Author: hzb
# @Date:   2020-11-13 16:23:41
# @Last Modified by:   hzb
# @Last Modified time: 2020-12-25 20:06:22
# --------------------------------------------------------
# DaSiamRPN
# Licensed under The MIT License
# Written by Qiang Wang (wangqiang2015 at ia.ac.cn)
# --------------------------------------------------------
#!/usr/bin/python
import glob, cv2, torch
from net import SiamRPNotb
from os.path import realpath, dirname, join, basename
from run_SiamRPN import SiamRPN_init, SiamRPN_track
from utils import get_axis_aligned_bbox, cxy_wh_2_rect
import sys
import os
import numpy as np
import time

def SiamRPN_load(image,boxes,txt_path):
    if not os.path.exists(txt_path):
        os.makedirs(txt_path)
    multiTracker = cv2.MultiTracker_create()
    net = SiamRPNotb()
    net.load_state_dict(torch.load(join(realpath(dirname(__file__)), 'SiamRPNOTB.model')))
    net.eval().cuda()
    states,labels=[],[]
    for bbox in boxes:
        #init_rbox = [bbox[0],bbox[1],bbox[0]+bbox[2],bbox[1],bbox[0]+bbox[2],bbox[1]+bbox[3],bbox[0],bbox[1]+bbox[3]]
        init_rbox = [bbox[0],bbox[1],bbox[2],bbox[1],bbox[2],bbox[3],bbox[0],bbox[3]]
        [cx, cy, w, h] = get_axis_aligned_bbox(init_rbox)
        # print(cx, cy, w, h,'-----',init_rbox)
        target_pos, target_sz = np.array([cx, cy]), np.array([w, h])
        states.append(SiamRPN_init(image, target_pos, target_sz, net))
        labels.append(bbox[-1])
    return states,labels
    
def siam_track(image,img_name,txt_path,states,labels,roi):
    x_min, y_min = roi[0], roi[1]
    x_max, y_max = roi[2], roi[3]
    # img_h, img_w = image.shape[0], image.shape[1]
    result_state=[]
    for state in states:
        state_o = SiamRPN_track(state, image)  # track
        result_state.append(state_o)
    txt=os.path.join(txt_path,img_name.replace('.jpg','.txt'))
    file_handle=open(txt,'w')
    mess=''
    del_list=[]
    for i,state in enumerate(result_state):
            res = cxy_wh_2_rect(state['target_pos'], state['target_sz'])
            res = [int(l) for l in res]
            if (res[0] + res[2])>x_max or (res[1] + res[3])>y_max or res[0]<x_min or res[1]<y_min:
                del_list.append(i)
            else:
                cv2.rectangle(image,(res[0],res[1]),(res[0]+res[2],res[1]+res[3]),(0,0,255), 2)
                cv2.putText(image,labels[i],(res[0],res[1]-5),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                mess+=f'{(res[0])} {res[1]} {res[0]+res[2]} {res[1]+res[3]} {labels[i]} \n'
    file_handle.write(mess)
    for i in reversed(del_list):
        del result_state[i]
        del labels[i]
    return result_state,image,labels

    
if __name__ == '__main__':
    txt_path =  '/media/mb/668452BE84529103/wmh/track_biaozhu/txt/'
    img_path= '/media/mb/668452BE84529103/wmh/track_biaozhu/img_7/'
    image_list=os.listdir(img_path)
    image_list.sort()
    image=cv2.imread(img_path+image_list[0])
    bboxes,colors=[],[]
    """
    while True:
        # 在对象上绘制边界框selectROI的默认行为是从fromCenter设置为false时从中心开始绘制框，可以从左上角开始绘制框
        bbox = cv2.selectROI('MultiTracker', image)
        bbox=list(bbox)
        print(bbox,'------')
        bbox.append('1')
        bboxes.append(bbox)
        colors.append((randint(64, 255), randint(64, 255), randint(64, 255)))
        print("Press q to quit selecting boxes and start tracking")
        print("Press any other key to select next object")
        k = cv2.waitKey(0) 
        if (k == 113):  # q is pressed
            break
    """
    bboxes=[[544, 196, 651, 407,'1'],[600,600,800,800,'2']]
    states,labels=SiamRPN_load(image,bboxes,txt_path)
    for i in image_list:
        image=cv2.imread(img_path+i)
        states,image=video_track(image,i,txt_path,states,labels)
        cv2.imshow('img',image)
        cv2.waitKey(1)
