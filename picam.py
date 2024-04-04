import numpy
import io
import os
import cv2
from picamera2 import Picamera2
from imutils import paths
import face_recognition
import pickle
import os

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

name = 'Jacob' #replace with your name
if (not os.path.isdir(name)):
    os.mkdir(name)
print(name)

cv2.namedWindow("press space for facial detection photo, press backspace to delete most recent, escape to finish", cv2.WINDOW_NORMAL)
cv2.resizeWindow("press space for facial detection photo, press backspace to delete most recent, escape to finish", 1200, 800)

img_counter = 0
while True:
    frame = picam2.capture_array()
    # if not ret:
    #     print("failed to grab frame")
    #     break
    cv2.imshow("press space for facial detection photo, press backspace to delete most recent, escape to finish", frame)

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
    elif k%256 == 8:
        # BACKSPACE pressed
        img_counter -= 1
        img_name = name +"/image_{}.jpg".format(img_counter)
        os.remove(img_name)
        print("{} deleted!".format(img_name))

cv2.destroyAllWindows()

# our images are located in the dataset folder
print("[INFO] processing faces from images just taken...")
imagePaths = list(paths.list_images(name))

# initialize the list of known encodings and known names
knownEncodings = []
knownNames = []

# loop over the image paths
for (i, imagePath) in enumerate(imagePaths):
	# extract the person name from the image path
	print("[INFO] processing image {}/{}, {}".format(i + 1,
		len(imagePaths), imagePath))
	#name = imagePath.split(os.path.sep)[-2]

	# load the input image and convert it from RGB (OpenCV ordering)
	# to dlib ordering (RGB)
	image = cv2.imread(imagePath)
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# detect the (x, y)-coordinates of the bounding boxes
	# corresponding to each face in the input image
	face_locations = face_recognition.face_locations(rgb)
	# compute the facial embedding for the face
	encodings = face_recognition.face_encodings(rgb, face_locations)

	# loop over the encodings
	for encoding in encodings:
		# add each encoding + name to our set of known names and
		# encodings
		knownEncodings.append(encoding)
		knownNames.append(name)

# dump the facial encodings + names to disk
print("[INFO] serializing encodings...")
data = {"encodings": knownEncodings, "names": knownNames}
f = open("encodings.pickle", "wb")
f.write(pickle.dumps(data))
f.close()