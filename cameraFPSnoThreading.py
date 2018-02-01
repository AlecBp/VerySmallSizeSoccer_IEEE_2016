import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)

while(True):
	tempo = time.time()
    # Capture frame-by-frame
	ret, frame = cap.read()

	if frame!=None:
		cv2.imshow('frame',frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

	print "FPS: ", 1/(time.time()-tempo)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()