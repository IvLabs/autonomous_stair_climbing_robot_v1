import time

from pydarknet import Detector, Image
import cv2

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Process a video.')
    parser.add_argument('path', metavar='video_path', type=str,
                        help='Path to source video')

    args = parser.parse_args()
    print("Source Path:", args.path)
    cap = cv2.VideoCapture(args.path)


    average_time = 0

    net = Detector(bytes("stairs-yolov3-tiny.cfg", encoding="utf-8"), bytes("stairs-yolov3-tiny_6500.weights", encoding="utf-8"), 0,
                   bytes("stairs-obj.data", encoding="utf-8"))

    while True:
        r, frame = cap.read()
        if r:
            start_time = time.time()

            # Only measure the time taken by YOLO and API Call overhead

            dark_frame = Image(frame)
            results = net.detect(dark_frame)
            del dark_frame

            end_time = time.time()
            fps = 1 / (end_time - start_time)
            
            print("FPS: ", fps)
            average_time = average_time * 0.8 + (end_time-start_time) * 0.2

            # print("Total Time:", end_time-start_time, ":", average_time)

            for cat, score, bounds in results:
                x, y, w, h = bounds
                print(x, y, w, h)
                cv2.rectangle(frame, (int(x-w/2),int(y-h/2)),(int(x+w/2),int(y+h/2)),(255,0,0))
                cv2.putText(frame, str(cat.decode("utf-8")), (int(x), int(y)), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0))

            cv2.imshow("preview", frame)

        k = cv2.waitKey(1)
        if k == 0xFF & ord("q"):
            break
