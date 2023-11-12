import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import time

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
classifier = Classifier("keras_model.h5","labels.txt")

offset = 20
imgSize = 300

folder = "data/C"
counter = 0

labels = ['1','2','3','4','5','6','7','8','9','0','Hello','Yes','No']
while True:
    success, img = cap.read()
    imgOutput = img.copy()
    hands, img = detector.findHands(img)
    if hands:
        hand = hands[0]
        x,y,w,h = hand['bbox']

        imgWhite = np.ones((imgSize,imgSize,3),np.uint8)*255
        imgCrop = img[y-offset : y+ h+offset,x-offset : x+w+offset]
        imgCropShape = imgCrop.shape
        Ratio  = h/w
        if Ratio >1:
            k = imgSize/h
            wCal  = math.ceil(k*w)
            imgResize = cv2.resize(imgCrop,(wCal, imgSize))
            imgResizeShape = imgResize.shape
            Wgap = math.ceil((imgSize-wCal)/2)
            imgWhite[:,Wgap:wCal+Wgap] = imgResize
            perdiction, index = classifier.getPrediction(imgWhite,draw=False)
            print(perdiction,index)
            
        else:
            k = imgSize/w
            hCal  = math.ceil(k*h)
            imgResize = cv2.resize(imgCrop,(imgSize, hCal))
            imgResizeShape = imgResize.shape
            hgap = math.ceil((imgSize-hCal)/2)
            imgWhite[hgap:hCal+hgap,:] = imgResize
            perdiction, index = classifier.getPrediction(imgWhite,draw=False)
        cv2.rectangle(imgOutput,(x-offset,y-offset-50),(x-offset+90,y-offset-50+50),(255,0,255),cv2.FILLED)
        cv2.putText(imgOutput,labels[index],(x,y-20),cv2.FONT_HERSHEY_COMPLEX,2,(255,255,255),2)
        cv2.rectangle(imgOutput,(x-offset,y-offset),(x+w+offset,y+h+offset),(255,0,255),2)

        #cv2.imshow('ImageCrop', imgCrop)
        cv2.imshow('ImageWhite',imgWhite)

    cv2.imshow("Image", imgOutput)
    cv2.waitKey(1)
