import numpy as np
import matplotlib as plt
import math
import cv2
import RPiInput_Cloud
import picamera
import time

cam = PiCamera()
i = 0
while ldr >= ldrthr:
    i = i + 1
    camera.start_preview()
    time.sleep(2)
    img = camera.capture('PrivateKeyFile%s.jpg' i)
else:
    camera.stop_preview()

def giveCoords(contours):
    arr = []
    #list of coordinates
    for aa in contours:
        approx = cv2.approxPolyDP(aa, 0.009 * cv2.arcLength(aa, True), True)'
        n = approx.ravel()
        #flattens the array into a 1D array
        ca = []
        i = 0
        for j in n:
            if(i % 2 == 0):
                x = n[i]
                y = n[i+1]
                ca.append((x, y))
            i = i + 1
        arr.append(ca)
        #contour coordinates list approximated added to the main list
    return arr
#taking in coordinates to calculate area covered


def Area2D(pts):
    #horizontally sequencing array(np.hstack)
    lines = np.hstack([pts, np.roll(pts, -1, axis=0)])
#calculating the area itself
    area = 0.5*abs(sum(x1*y2-x2*y1 for x1, y1, x2, y2 in lines))
    return area
#find permieter of area covered by points passed in args


def perim(pt):
    pt.append(pt[0])
    per = 0
    for i in range(0, len(pts)-1):
        per = per + math.hypot(pt[i][0]-pt[i+1][0], pt[i][1]-pt[i+1][1])
    return per
#hypot finds hypotenuse given perpendicular side and base
#FTE = feature to extract data


def FTE(imgpath):
    img = cv2.imread(imgpath, 0)
    kernel = np.ones((5, 5), np.uint8)
    colouredimg = cv2.imread(imgpath)
    ogimg = cv2.imread(imgpath)
    #Blank image for morphology
    openimg = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    #opening img
    erodedimg = cv2.erode(openimg, kernel, iterations=1)
    #eroding img
    dilatedimg = cv2.dilate(erodedimg, kernel, iterations=1)
    #dilating
    closed = cv2.morphologyEx(dilatedimg, cv2.MORPH_CLOSE, kernel)
    #Gausian blur filter added to img
    blur = cv2.GaussianBlur(erodedimg, (5, 5), 0)
    blur = ~blur
    #Image inversion to remove holes that may interfere with interpretation
    #find threshold using img with gaussian blur
    ret, thresholdval = cv2.threshold(
        blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    #find contours of inverted img
    contours, hierarchy = cv2.findContours(
        thresholdval, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #drawing contour points after recalculation
    cv2.drawContours(colouredimg, contours, -1, (0, 0, 255), 2)