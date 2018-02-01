import cv2
import numpy as np
from matplotlib import pyplot as plt
image = cv2.VideoCapture(0)
ret, frame = image.read()
#changing the colorspace from BGR->RGB
if frame != None:
	input = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB )
	rows,cols,channels = input.shape
	points1 = np.float32([[100,100],[300,100],[100,300]])
	points2 = np.float32([[200,150],[400,150],[100,300]])
	A = cv2.getAffineTransform(points1,points2)
	output = cv2.warpAffine(input,A,(cols,rows))
	plt.subplot(121),plt.imshow(input),plt.title('Input')
	plt.subplot(122),plt.imshow(output),plt.title('Affine Output')
	plt.show()

	cv2.waitKey(0)
	cv2.destroyAllWindows()
	cam.release()