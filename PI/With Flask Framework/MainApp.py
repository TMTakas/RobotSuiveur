#!/usr/bin/env python
from flask import Flask, render_template, Response
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import io
import os
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import mysql.connector
from threading import Thread

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(2)
steam = io.BytesIO()

lowerBoundGreen=np.array([51,37,0])
upperBoundGreen=np.array([94,234,213])

lowerBoundRed=np.array([0, 115, 108])
upperBoundRed=np.array([179, 255, 247])

kernelOpen=np.ones((5,5))
kernel = np.ones((5,5), np.uint8)

WhatToSend = 1

mydb = mysql.connector.connect(
  host="localhost",
  user="mondir",
  passwd="035896",
  database="robot"
)
mycursor = mydb.cursor()

def getValuesFromDb():
    global WhatToSend
    global lowerBoundGreen
    global upperBoundGreen
    global lowerBoundRed
    global upperBoundRed
    while True:
        time.sleep(0.1)
        mycursor.execute("SELECT * FROM sett")
        myresult = mycursor.fetchall()
        for x in myresult:
            WhatToSend = int(x[1])
            lowerBoundGreen = np.array([ int(x[3]), int(x[2]), int(x[4]) ])
            upperBoundGreen = np.array([ int(x[6]), int(x[5]), int(x[7]) ])
            lowerBoundRed = np.array([ int(x[9]), int(x[8]), int(x[10]) ])
            upperBoundRed = np.array([ int(x[12]), int(x[11]), int(x[13]) ])
        mydb.commit()


def drawToImage(img, x, y, w, h):
    cv2.rectangle(img, (x, y), (x + x, y + h), (255,0,0), 2)
    return

def finTheBiggest(conts):
    wFinal = -1
    hFinal = -1
    cont = None
    index = -1
    for i in range(len(conts)):
        x,y,w,h=cv2.boundingRect(conts[i])
        if w > wFinal and h > hFinal:
            wFinal = w
            hFinal = h
            cont = conts[i]
            index = i
    return cont, index

def findBestGreenByRed(img, contsGreenRed):
    reds = []

    for i in range(len(contsGreenRed)):
        reds.append(contsGreenRed[i][1])

    cont, index = finTheBiggest(reds)
    if(index != -1):
        return contsGreenRed[index]
    else:
        return None

def findTheBiggestRedInGreens(contsGreenReds):
    greenRed = []
    for i in range(len(contsGreenReds)):
        cont, tmp = finTheBiggest(contsGreenReds[i][1])
        greenRed.append((contsGreenReds[i][0], cont))
    return greenRed

def findAllGreensWithRed(contsGreen, contsRed):
    contsGreenReds = []

    for i in range(len(contsGreen)):
        contsReds = []

        #Green
        xG,yG,wG,hG=cv2.boundingRect(contsGreen[i])
        P1G = [xG, yG]
        P2G = [xG + wG, yG]
        P3G = [xG + wG, yG + hG]
        P4G = [xG, yG + hG]

        for j in range(len(contsRed)):   

            #Red
            xR,yR,wR,hR=cv2.boundingRect(contsRed[j])
            P1R = [xR, yR]
            P2R = [xR + wR, yR]
            P3R = [xR + wR, yR + hR]
            P4R = [xR, yR + hR]

            if P1R[0] > P1G[0] and P1R[1] > P1G[1] and P2G[0] > P2R[0] and P2G[1] < P2R[1] and P3G[0] > P3R[0] and P3G[1] > P3R[1] and P4G[0] < P4R[0] and P4G[1] > P4R[1]:
                contsReds.append(contsRed[j])
        
        if len(contsReds) > 0:
            contsGreenReds.append((contsGreen[i], contsReds))
    return contsGreenReds

app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen():
    """Video streaming generator function."""
    global WhatToSend
    global lowerBoundGreen
    global upperBoundGreen
    global lowerBoundRed
    global upperBoundRed
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        
        img = image
        imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

        maskGreen = cv2.inRange(imgHSV,lowerBoundGreen,upperBoundGreen) 
        morphologyExGreen = cv2.morphologyEx(maskGreen,cv2.MORPH_OPEN, kernelOpen) 
        erosionGreen = cv2.erode(morphologyExGreen, kernel, iterations=1)

        maskRed = cv2.inRange(imgHSV,lowerBoundRed,upperBoundRed) 
        morphologyExRed = cv2.morphologyEx(maskRed,cv2.MORPH_OPEN, kernelOpen) 
        erosionRed = cv2.erode(morphologyExRed, kernel, iterations=1)

        t, contsGreen, hierarchyGreen = cv2.findContours(erosionGreen.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)   
        t, contsRed, hierarchyRed = cv2.findContours(erosionRed.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

        contsGreenReds = findAllGreensWithRed(contsGreen, contsRed)
        contsGreenRed = findTheBiggestRedInGreens(contsGreenReds)
        contGreenRed = findBestGreenByRed(img, contsGreenRed)

        if contGreenRed != None:
            xG,yG,wG,hG=cv2.boundingRect(contGreenRed[0])
            xR,yR,wR,hR=cv2.boundingRect(contGreenRed[1])
            cv2.rectangle(img, (xG, yG), (xG + wG, yG + hG), (0,255,0), 2)
            cv2.rectangle(img, (xR, yR), (xR + wR, yR + hR), (0,0,255), 2)

        if WhatToSend == 1:
            cv2.imwrite('t.jpg', img)
        elif WhatToSend == 2:
            cv2.imwrite('t.jpg', erosionGreen)
        elif WhatToSend == 3:
            cv2.imwrite('t.jpg', erosionRed)

        rawCapture.truncate(0)
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    thread = Thread(target = getValuesFromDb, args = ())
    thread.start()
    app.run(host='192.168.43.82', debug=False, threaded=True)