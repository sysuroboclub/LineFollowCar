import cv2 as cv
import numpy as np
import serial
import os
import math
import time

print(cv.__version__)
cam = cv.VideoCapture(0)

# open serial port
# ser=serial.Serial('COM3',115200)

print(cam.set(cv.CAP_PROP_FRAME_WIDTH, 1280))
print(cam.set(cv.CAP_PROP_FRAME_HEIGHT, 720))
if not cam.isOpened():
    print("Cannot open camera")
    exit()

while True:
    beginTime = time.perf_counter()

    # Read the frame
    ret, frame = cam.read()
    rows, cols, _ = frame.shape
    M = cv.getRotationMatrix2D((cols/2, rows/2), 180, 1)
    frame = cv.warpAffine(frame, M, (cols, rows))
    frameres = cv.resize(frame, (int(cols/2), int(rows/2)))
    # info=ser.read(100)

    # Down scale

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Change to gray
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    rows, cols = gray.shape
    gray = cv.resize(gray, (int(cols/2), int(rows/2)))
    rows, cols = gray.shape
    gray = cv.GaussianBlur(gray, (15, 15), sigmaX=3)

    # Rotate
    # M=cv.getRotationMatrix2D((cols/2,rows/2),180,1)
    # gray=cv.warpAffine(gray,M,(cols,rows))

    # Crop the img (y,x)
    # gray=gray[180:540,210:700]
    # The numbers are magic number!!!!!
    # gray=gray[90:270,105:350]

    # Binarization
    ret, gray = cv.threshold(gray, 40, 255, cv.THRESH_OTSU)
    edges = cv.Canny(gray, 200, 300)
    # grad_y=cv.Sobel(gray,cv.CV_8U,0,1,ksize=3,scale=1,delta=0,borderType=cv.BORDER_DEFAULT)
    # edges=cv.Scharr(edges,cv.CV_8U,0,1)
    kernel = np.ones((3, 3), np.uint8)
    edges = cv.morphologyEx(edges, cv.MORPH_DILATE, kernel)
    lines = cv.HoughLinesP(edges, cv.HOUGH_PROBABILISTIC,
                           np.pi/180, 30, minLineLength=60, maxLineGap=3)
    for x in range(0, len(lines)):
        for x1, y1, x2, y2 in lines[x]:
            #cv2.line(inputImage,(x1,y1),(x2,y2),(0,128,0),2, cv2.LINE_AA)
            pts = np.array([[x1, y1], [x2, y2]], np.int32)
            cv.polylines(frameres, [pts], True, (0, 255, 0))
    # ws=cv.watershed()

    # begin=0
    # end=0
    # points=[]
    # res=[]
    # # # Easy way to find the edge of line
    # it=np.nditer(edges,flags=['multi_index'])
    # prev=0
    # while not it.finished:
    #     if it[0]!=prev:
    #         points.append(it.multi_index)
    #     prev=it[0]
    #     it.iternext()
    # for i in points:
    #     points

    # # Draw point
    # for k in res:
    #     res=cv.circle(res,(k[0],k[1]),4,127,thickness=4)

    # measure time
    print(int(1/(time.perf_counter()-beginTime)))

    # How to send serial string
    # strtmp=str(123)+'\n'
    # ser.write(strtmp.encode())

    # Show the img
    cv.imshow('img', gray)
    cv.imshow('result', edges)
    cv.imshow('color', frameres)
    # Press q to quit
    if cv.waitKey(1) == ord('q'):
        break
    # Press s to save image to ./
    elif cv.waitKey(1) == ord('s'):
        cv.imwrite('anyway.png', gray)
        print('saved')
    elif cv.waitKey(1) == ord('e'):
        cv.imwrite('edges.png', edges)
        print('edges saved')
print(edges)
print(lines)
ks=[]
for line in lines:
    line=line[0]
    ks.append((line[1]-line[3])/(line[0]-line[2]))
print(ks)
cv.destroyAllWindows()
