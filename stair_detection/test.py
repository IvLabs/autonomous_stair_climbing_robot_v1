from py_yolo import object_detector
import cv2

cv2.namedWindow('Output', cv2.WINDOW_NORMAL)
image = cv2.imread('/home/nvidia/darknet/data/test/IMG_20181029_142711.jpg')
output = object_detector(image)
for bounds in output:
	x, y, w, h = bounds
	cv2.rectangle(image, (int(x-w/2),int(y-h/2)),(int(x+w/2),int(y+h/2)),(255,0,0))
	cv2.putText(image, 'stair', (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0))
	
cv2.imshow('Output', image)
cv2.waitKey(0)
