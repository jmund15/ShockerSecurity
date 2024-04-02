#! /usr/bin/python

# import the necessary packages
from picamera2 import Picamera2, MappedArray, Preview
from imutils import paths
import os
import face_recognition
import imutils
import pickle
import time
import cv2
import keyboard

#Determine faces from encodings.pickle file model created from train_model.py
known_dir = "KnownFaces"
encodingsP = known_dir + "/encodings.pickle"
unknown_dir = "UnknownFaces"
if (not os.path.isdir(unknown_dir)):
    os.mkdir(unknown_dir)

# load the known faces and embeddings
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(encodingsP, "rb").read())


boxes = []
encodings = []
names = []
unknown_num = len(list(paths.list_images(unknown_dir))) + 1
print("unknown num: {}".format(unknown_num))
#Initialize 'currentname' to trigger only when a new person is identified.
currentname = "Unknown"

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480),}))#, lores={"size": (320, 240), "format": "YUV420"}))
picam2.start_preview(Preview.QTGL, width=1280, height=960)

(w0, h0) = picam2.stream_configuration("main")["size"] 
#(w1, h1) = picam2.stream_configuration("lores")["size"]

#cv2.namedWindow("Facial Detection", cv2.WINDOW_NORMAL)
#cv2.resizeWindow("Facial Detection", 1200, 800)

def draw_faces(request):
	global unknown_num
	with MappedArray(request, "main") as m:
		# loop over the facial embeddings
		for encoding in encodings:
			# attempt to match each face in the input image to our known
			# encodings
			matches = face_recognition.compare_faces(data["encodings"],
				encoding)
			name = "Unknown" #if face is not recognized, then print Unknown

			# check to see if we have found a match
			if True in matches:
				# find the indexes of all matched faces then initialize a
				# dictionary to count the total number of times each face
				# was matched
				matchedIdxs = [i for (i, b) in enumerate(matches) if b]
				counts = {}

				# loop over the matched indexes and maintain a count for
				# each recognized face face
				for i in matchedIdxs:
					name = data["names"][i]
					counts[name] = counts.get(name, 0) + 1

				# determine the recognized face with the largest number
				# of votes (note: in the event of an unlikely tie Python
				# will select first entry in the dictionary)
				name = max(counts, key=counts.get)

				#If someone in your dataset is identified, print their name on the screen
				#if currentname != name:
				#	currentname = name
				#	print(currentname)
				#else:
				#	currentname = "Unknown"
			else:
				print("unknown face detected! Send picture to user!")
				print("unknown num: {}".format(unknown_num))
				cv2.imwrite("{0}/unknown_{1}.jpg".format(unknown_dir, unknown_num), rgb)
				unknown_num += 1
			# update the list of names
			names.append(name)

		# loop over the recognized faces
		for ((top, right, bottom, left), name) in zip(boxes, names):
			# (x, y, w, h) = [c * n // d for c, n, d in zip(f, (w0, h0) * 2, (w1, h1) * 2)]            
			# cv2.rectangle(m.array, (x, y), (x + w, y + h), (0, 255, 0, 0))
			
			# draw the predicted face name on the image - color is in BGR
			cv2.rectangle(m.array, (left, top), (right, bottom),
				(0, 255, 225), 0)
			y = top - 15 if top - 15 > 15 else top + 15
			cv2.putText(m.array, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
				.8, (0, 255, 255), 0)
				
picam2.post_callback = draw_faces
picam2.start(show_preview = True)
# loop over frames from the video file stream
while True:
	# grab the frame from the threaded video stream and resize it
	# to 500px (to speedup processing)
	frame = picam2.capture_array()
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	# Detect the fce boxes
	boxes = face_recognition.face_locations(rgb)
	# compute the facial embeddings for each face bounding box
	encodings = face_recognition.face_encodings(rgb, boxes)
	names = []
	
	
	#if keyboard.is_pressed('q'):
	#	break
	# display the image to our screen
	#cv2.imshow("Facial Detection", frame)
	#key = cv2.waitKey(1)# & 0xFF
	#if key%256 == 27:
	#	break
	# quit when 'q' key is pressed
	#if key == ord("q"):
    #	break


# do a bit of cleanup
cv2.destroyAllWindows()
picam2.stop_preview()
picam2.stop()



