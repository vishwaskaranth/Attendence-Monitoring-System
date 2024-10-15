from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import cv2 
import os

import numpy as np
cv2.VideoCapture(0)
face_detector1=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#eye_detector1 = cv2.CascadeClassifier('haarcascade_eye.xml')

cap =cv2.VideoCapture(0)
#cap =cv.VideoCapture('Datadet/view.mp4')
while True:
    isTrue, frame = cap.read() #reading frame by frame

    cv2.imshow('Video',frame)
   # if cv.waitKey(20) & 0xFF==ord('d'): #if d is pressed operation breaks
    #    break
    cap.release()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces_result = face_detector1.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces_result:
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
#eyes = eye_detector1.detectMultiScale(roi_gray)
#for (ex,ey,ew,eh) in eyes:
    #cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()


