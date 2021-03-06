#!/usr/bin/python
# encoding: utf-8

from helper import *
import cv2
import numpy as np


# https://klassenresearch.orbs.com/Plotting+with+Python
from matplotlib import rc
# Make use of TeX﻿
rc('text',usetex=True)
# Change all fonts to 'Computer Modern'
rc('font',**{'family':'serif','serif':['Computer Modern']})

fileName = "yawLog25"

capture = cv2.VideoCapture(fileName+".mp4")

dataLog = loadFromFile("",fileName+".p")

#frame_hsv = 0

def my_mouse_callback(event,x,y,flags,param):
    global frame_hsv
    if event == cv2.cv.CV_EVENT_LBUTTONUP:
        print("Color:")
        print(frame_hsv[y,x])

cv2.namedWindow("image")
cv2.setMouseCallback("image",my_mouse_callback)

pos_avg = np.zeros(2)

dataLog['videoTimestamp'] = []
dataLog['pos'] = []

first = True
while True:
    key_pressed = cv2.waitKey(1)    #Escape to exit
    if key_pressed == 27:
        exit()
    if key_pressed == 65363:
        capture.set(cv2.cv.CV_CAP_PROP_POS_MSEC,299.9)
#        for i in xrange(30): # skip frames
#            flag = capture.grab()
#            if flag == False:
#                exit()
    
    elapsedTime = capture.get(cv2.cv.CV_CAP_PROP_POS_MSEC)/1000.
    
    flag, frame = capture.read()
    if flag == False:
        break
    
# convert to hsv and find range of colors
    frame_hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
    GREEN_MIN = np.array([73-20, 50, 50],np.uint8)
    GREEN_MAX = np.array([73+20, 255, 255],np.uint8)
    thresh = cv2.inRange(frame_hsv,GREEN_MIN,GREEN_MAX)
    
    #cv2.imshow("image", thresh)
    
    # find contours in the threshold image
    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)#cv2.CHAIN_APPROX_SIMPLE)

    # finding contour with maximum area and store it as best_cnt
    max_area = 0
    best_cnt = None
    for cnt in contours:
        area = cv2.contourArea(cnt)
    
        if area > max_area:
            max_area = area
            best_cnt = cnt
    if best_cnt != None:
        #print(best_cnt)
        #print(best_cnt.shape)
        best_cnt = np.mean(best_cnt,axis=0)
        while len(best_cnt.shape) > 1:
            best_cnt = best_cnt[0]
        best_cnt[1] *= -1
        pos_avg = pos_avg*0.9 + best_cnt*0.1
        if first:
            first = False
            pos_avg = best_cnt
        print pos_avg
        dataLog['videoTimestamp'].append(elapsedTime)
        dataLog['pos'].append(pos_avg)

saveToFile(dataLog,"",fileName+"_withPos.p")

