import cv2 as cv
import numpy as np
import serial 
import os
import math
import time

print(cv.__version__)
cam=cv.VideoCapture(0)

# open serial port
ser=serial.Serial('COM3',115200)
# ser.open()
print(cam.set(cv.CAP_PROP_FRAME_WIDTH,1920))
print(cam.set(cv.CAP_PROP_FRAME_HEIGHT,1080))
if not cam.isOpened():
    print("Cannot open camera")
    exit()

while True:
    beginTime=time.perf_counter()

    #Read the frame
    ret,frame=cam.read()
    
    # info=ser.read(100)

    #Down scale
    frame=cv.resize(frame,(480,270))

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    #Change to gray
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    rows,cols=gray.shape

    #Rotate
    # M=cv.getRotationMatrix2D((cols/2,rows/2),180,1)
    # gray=cv.warpAffine(gray,M,(cols,rows))

    # Crop the img (y,x)
    # gray=gray[180:540,210:700]
    gray=gray[90:270,105:350]

    # Binarization
    ret,gray=cv.threshold(gray,127,255,cv.THRESH_OTSU)
    
    # measure time
    print((time.perf_counter()-beginTime))

    # How to send serial string
    # strtmp=str(123)+'\n'
    # ser.write(strtmp.encode())
    
    #Show the img
    cv.imshow('img', gray)
    # cv.imshow('edges',edges)
    if cv.waitKey(1) == ord('q'):
        break
    if cv.waitKey(1) == ord('s'):
        cv.imwrite('anyway.png',gray)
        print('saved')
cv.destroyAllWindows()