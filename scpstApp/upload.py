#from picamera2 import Picamera2
from bucketAPI import *
import time
import cv2 as cv
import subprocess


#picam2 = Picamera2()
#start = time.time()
#picam2.start_and_capture_file('tookwithpi.jpg')
#end = time.time()
#print('capture took', end - start)

def f():
	command = ['libcamera-still', '-o', 'tookwithpi.jpg', '--autofocus-range', 'normal']
	try:
		subprocess.run(command, check=True)
		print('success')
	except:
		print('fail')


	im = cv.imread('tookwithpi.jpg')
	(y, x, z) = im.shape
	print(y, x, z)
	y = int(y / 6)
	x = int(x / 6)
	im = cv.resize(im, (x,y))
	print(im.shape)
	cv.imwrite('Resized.jpg', im) 

	start2 = time.time()
	upload_to_bucket('Resized.jpg', 'fromthepi.jpg')
	end2 = time.time()

	print('Upload took', end2 - start2)


while True:
	f()
	time.sleep(30)
