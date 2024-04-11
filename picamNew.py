import numpy
import io
import os
import cv2
from picamera2 import Picamera2
from imutils import paths
import pickle
import os
import encode

picam2 = Picamera2()
picam2.start()


while (True):
    name = input("Enter name of person to be added to the database: ")
    if (not os.path.isdir(name)):
        confirm = input("Name entered is " + name + ". Is this correct? (y/n)")
        if (confirm.lower() == 'y'):
            os.mkdir(name)
            break
        else:
            continue
    else:
        confirm = input("Name already has training, do you want to overwrite? (y/n)")
        if (confirm.lower() == 'y'):
            break
        else:
            continue
write_dir = "KnownFaces";         
print("Encoding face for: " + name + "!")
print("INSTRUCTIONS: Press space to take photo for facial detection training, press backspace to delete most recent, escape to finish")
print("Try to get multiple angles of face for maximum accuracy. Make sure you are the only face in the picture.")

windowName = "Training"
cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
cv2.resizeWindow(windowName, 500, 300)

img_counter = 0
while True:
    frame = picam2.capture_array()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # if not ret:
    #     print("failed to grab frame")
    #     break
    cv2.imshow("press space for facial detection photo, press backspace to delete most recent, escape to finish", rgb)

    k = cv2.waitKey(1)
    if k%256 == ord("q"):
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = name +"/image_{}.jpg".format(img_counter)
        cv2.imwrite(img_name, rgb)
        print("{} written!".format(img_name))
        img_counter += 1
    elif k%256 == 8:
        # BACKSPACE pressed
        img_counter -= 1
        img_name = name +"/image_{}.jpg".format(img_counter)
        os.remove(img_name)
        print("{} deleted!".format(img_name))

cv2.destroyAllWindows()

# our images are located in the dataset folder
print("[INFO] processing faces from images just taken...")
encode.encode_faces(name, write_dir, name)
