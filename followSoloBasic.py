import cv2 as cv
import numpy as np
import serial 
import os
import math
import time

print(cv.__version__)
cam=cv.VideoCapture(0)

# open serial port
#ser=serial.Serial('COM3',115200)

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
    # The numbers are magic number!!!!!
    gray=gray[90:270,105:350]

    # Binarization
    ret,gray=cv.threshold(gray,127,255,cv.THRESH_OTSU)
    
    begin=0
    end=0
    points=[]
    rows,cols=gray.shape
    # Easy way to find the edge of line
    for j in range(rows-1,0,-1):
        for i in range(0,cols-1):
            if gray[j,i]==0 and gray[j,i+1]==255:
                end=i
            if gray[j,i]==255 and gray[j,i+1]==0:
                begin=i
        # Filter of distance between edge
        distance=end-begin
        # Middle of line
        xCoor=int(begin/2+end/2)

        # Neighbor point shouldn't be far. 
        if distance>10 and distance<50:
            if len(points)>0:
                if math.sqrt(((xCoor-points[-1][0])**2)+((j-points[-1][1])**2))<10:
                    points.append([xCoor,j])
            else:
                points.append([xCoor,j])
    res=gray

    # Draw point
    for k in points:
        res=cv.circle(res,(k[0],k[1]),4,127,thickness=4)

    # measure time
    print((time.perf_counter()-beginTime))

    # How to send serial string
    # strtmp=str(123)+'\n'
    # ser.write(strtmp.encode())
    
    #Show the img
    cv.imshow('img', gray)
    cv.imshow('result',res)
    # Press q to quit
    if cv.waitKey(1) == ord('q'):
        break
    # Press s to save image to ./
    if cv.waitKey(1) == ord('s'):
        cv.imwrite('anyway.png',gray)
        print('saved')
cv.destroyAllWindows()