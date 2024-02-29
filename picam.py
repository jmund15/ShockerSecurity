import numpy
import io
import os
import cv2
from picamera2 import Picamera2

picam2 = Picamera2()
picam2.start()


name = 'Jacob' #replace with your name
if (not os.path.isdir(name)):
    os.mkdir(name)
print(name)

cv2.namedWindow("press space to take a photo", cv2.WINDOW_NORMAL)
cv2.resizeWindow("press space to take a photo", 500, 300)

img_counter = 0

while True:
    frame = picam2.capture_array()
    # if not ret:
    #     print("failed to grab frame")
    #     break
    cv2.imshow("press space to take a photo", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = name +"/image_{}.jpg".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cv2.destroyAllWindows()