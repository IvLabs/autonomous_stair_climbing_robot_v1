import pydarknet

net = pydarknet.Detector(bytes("stairs-yolov3-tiny.cfg", encoding="utf-8"), bytes("stairs-yolov3-tiny_6500.weights", encoding="utf-8"), 0, bytes("stairs-obj.data", encoding="utf-8"))

def object_detector(img):
	dark_frame = pydarknet.Image(img)
	results = net.detect(dark_frame)
	del dark_frame
	
	op = list()
	for cat, score, bounds in results:
		x, y, w, h = bounds
		op.append([x, y, w, h])
	
	return op
	
if __name__ == '__main__':
	import cv2
	cv2.namedWindow('Output', cv2.WINDOW_NORMAL)
	image = cv2.imread('/home/nvidia/darknet/data/test/IMG_20180821_220331.jpg')
	output = object_detector(image)
	for bounds in output:
		x, y, w, h = bounds
		cv2.rectangle(image, (int(x-w/2),int(y-h/2)),(int(x+w/2),int(y+h/2)),(255,0,0))
		cv2.putText(image, 'stair', (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0))
		
	cv2.imshow('Output', image)
	cv2.waitKey(0)
