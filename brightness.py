import os
import cv2
import math
import numpy as np

imgpath = '/assets/imgbuffer.png'
dir_path = os.path.dirname(os.path.realpath(__file__))
imgName = dir_path + imgpath

img = cv2.imread(imgName)
param = [0.114, 0.587, 0.299]
result = 0
for i in range(3):
    histr = cv2.calcHist([img],[i],None,[256],[0,256])
    result += np.argmax(histr)**2 * param[i]
print math.sqrt(result)
