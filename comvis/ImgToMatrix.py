############ testing with picture in matrix form

import numpy as np
import cv2

img = cv2.imread('2.jpg',0)
cv2.imshow('gray scale',img)


for i in range(100): 
	print img[i]




cv2.waitKey(0)

