import cv2
import numpy as np
# initialize the camera
cam = cv2.VideoCapture(0)


#in HSV
blue_min = (90,100,100)
blue_max = (120,255,255)

while (True):
	ret, frame = cam.read()
	
	if ret:

		cv2.imwrite("teste.png",frame)
		frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		frame_HSV = cv2.medianBlur(frame_HSV, 5)

		blueMask = cv2.inRange(frame_HSV, blue_min, blue_max)

		x = cv2.erode(blueMask, None, iterations=1)
		x = cv2.dilate(x, None, iterations=1)


		cv2.imshow("blue MASK", blueMask)
		cv2.imshow('VideoStream', frame)
		cv2.imshow("x", x)
	if cv2.waitKey(1) & 0xFF == ord("q"):
		break



# When everything done, release the capture
cam.release()
cv2.destroyAllWindows()