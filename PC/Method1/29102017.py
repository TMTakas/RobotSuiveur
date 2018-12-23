import cv2
import threading
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Lock 
import random
import time
import numpy as np
import sys

camera = PiCamera()
camera.resolution = (640, 480)
#camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
threshold = 0.6
fileName = "patern.png"
templateOrg = cv2.imread(fileName, 0)
image = cv2.imread(fileName, 0)
img_gray = cv2.imread(fileName, 0)
wO,hO = templateOrg.shape[::-1]
read_lock = Lock()
max_vals = [0,0,0,0,0,0,0,0,0,0]
top_lefts = [None, None, None, None, None, None, None, None, None, None]
bottom_rights = [None, None, None, None, None, None, None, None, None, None]
listThreads = []
templatesResized = []

def cameraThread():
	global image
	global max_vals
	global top_lefts
	global bottom_rights
	global threshold
	global img_gray
	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		image = frame.array
		img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		found = False
		i = -1
		for i in range(0, 10):
			if max_vals[i] >= threshold:
				cv2.rectangle(image, top_lefts[i], bottom_rights[i], 255, 2)
				found = True
				break
		print("\033[H\033[J")
		string = ""
		if found == True:
			string = string + "*** Thread " + str(i) + " Is Detecting " + str(max_vals[i]) + "\n\n\n"
		for i in range(0, 10):
			string = string + "- Thread " + str(i) + " Is Detecting " + str(max_vals[i]) + "\n"
		print(string)
		cv2.imshow("Image", image)	
		#cv2.imshow("img_gray", img_gray)	
		key = cv2.waitKey(1) & 0xFF
		rawCapture.truncate(0)
		if key == ord("q"):
			break
	return

def detectThread(index, sizeS):
	global image
	global max_vals
	global top_lefts
	global bottom_rights
	global threshold
	global templateOrg
	global img_gray
	while True:
		template = templatesResized[index]
		res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
		min_val, max_val,min_loc, max_loc = cv2.minMaxLoc(res)
		top_left = max_loc
		w,h = template.shape[::-1]
		bottom_right = (top_left[0] + w, top_left[1] + h)
		max_vals[index] = max_val
		#if max_val > threshold:
		#	print("The Thread {} Detecting {} On Size {}".format(index, max_val, sizeS))
		top_lefts[index] = top_left
		bottom_rights[index] = bottom_right
	return
	
cv2.imshow("templateOrg", templateOrg)

cameraT = threading.Thread(target = cameraThread, args = [])
cameraT.start()

for i in range(0, 10):
	template = cv2.resize(templateOrg, (0,0), fx=float((10-i)/10), fy=float((10-i)/10))
	templatesResized.append(template)
	
	
for i in range(0, 10):
	t = threading.Thread(target = detectThread, args = (i, float((10-i)/10)))
	listThreads.append(t)
	t.start()
		
for i in range(0, 10):
	listThreads[i].join()

cameraT.join()
