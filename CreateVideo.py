
import cv2
import numpy as np
import glob
 
img_array = []
for filename in sorted(glob.glob('DataImages/*png')):
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
 
#out = cv2.VideoWriter('project.avi',cv2.VideoWriter_fourcc(*'DIVX'), 20, size)
out = cv2.VideoWriter('Timelapse/project.mp4',cv2.VideoWriter_fourcc(*'MP4V'), 15, size)

 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()