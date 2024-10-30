#! /usr/bin/python

# import the necessary packages
#from picamera2 import Picamera2, MappedArray, Preview
import numpy as np
from imutils import paths
import os
#import face_recognition
#import imutils
import pickle
import time 
#import keyboard
from flask import Flask, Blueprint
from flask import render_template, url_for, flash, request, redirect, Response
from flask_login import LoginManager, login_required, current_user, logout_user

import sqlite3
import time
import numpy as np
import cv2

from flaskModels import CSRFForm
from flaskLogin import login_manager
from SQLiteConnect import matchEncodings, addFace

stream = Blueprint('stream', __name__, template_folder='../frontend')
#login_manager = LoginManager()
#login_manager.init_app(stream)
# app = Flask(__name__)
# app.debug=True

face_dir = '../frontend/static'
boxes = []
encodings = []
names = []
unknown_num = len(list(paths.list_images(face_dir))) + 1 #TODO: FIX!
print("unknown num: {}".format(unknown_num))
#Initialize 'currentname' to trigger only when a new person is identified.
currentname = "Unknown"

# def init_video():
#     data = load_known_face_encodings()

#     boxes = []
#     encodings = []
#     names = []
#     unknown_num = len(list(paths.list_images(unknown_dir))) + 1
#     print("unknown num: {}".format(unknown_num))
#     #Initialize 'currentname' to trigger only when a new person is identified.
#     currentname = "Unknown"

#     picam2 = Picamera2()
#     picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480),}))#, lores={"size": (320, 240), "format": "YUV420"}))
#     picam2.start_preview(Preview.QTGL, width=1280, height=960)
#     dest_dir = "MemberVideo"
#     #picam2.start_and_record_video("memberVideo.mp4", duration=5)

#     (w0, h0) = picam2.stream_configuration("main")["size"] 
#     #(w1, h1) = picam2.stream_configuration("lores")["size"]


@stream.route('/stream', methods=['GET'])
@login_required
def show():
    form = CSRFForm()
    #print('STREAMING HTML LOAD!')
    return render_template('stream.html', title='ShockerSecurity', form=form)


# @stream.route('/stream/security_footage')
# @login_required  # Protect the video feed route
# def stream_footage():
# 	return Response(get_footage(),mimetype='multipart/x-mixed-replace; boundary=frame')

# def load_known_face_encodings():
#     # load the known faces and embeddings
#     print("[INFO] loading encodings + face detector...")
#     #Determine faces from encodings.pickle file model created from train_model.py
    
#     #faces_data = []
#     data = {}
#     for fn in os.listdir(known_dir):
#         if fn.endswith('.pickle'):
#             path = os.path.join(known_dir, fn)
#             face = pickle.loads(open(path, "rb").read())
#             for key, value in face.items():
#                 if key in data:
#                     data[key].extend(value)
#                 else:
#                     data[key] = value
#     return data


# def draw_faces(request):
#     global data
#     global names
#     global encodings
#     global boxes
#     global unknown_num

#     with MappedArray(request, "main") as m:
#         # loop over the facial embeddings
#         for encoding in encodings:
            
#             #matches = []
#             #for data in faces_data:
#             #    matches += face_recognition.compare_faces(data["encodings"],
#             #	encoding)
#             # attempt to match each face in the input image to our known
#             # encodings
            
#             matches, name = matchEncodings(encoding)
#             if matches is None:
#                 #TODO: UNKNOWN TIMER
#                 print("unknown face detected! Send picture to user!")
#                 print("unknown num: {}".format(unknown_num))
#                 cv2.imwrite("{0}/unknown_{1}.jpg".format(unknown_dir, unknown_num), rgb)
#                 unknown_num += 1
#             else:
#                 # find the indexes of all matched faces then initialize a
#                 # dictionary to count the total number of times each face
#                 # was matched
#                 matchedIdxs = [i for (i, b) in enumerate(matches) if b]
#                 counts = {}

#                 # loop over the matched indexes and maintain a count for
#                 # each recognized face face
#                 for i in matchedIdxs:
#                     name = data["names"][i]
#                     counts[name] = counts.get(name, 0) + 1

#                 # determine the recognized face with the largest number
#                 # of votes (note: in the event of an unlikely tie Python
#                 # will select first entry in the dictionary)
#                 name = max(counts, key=counts.get)

#                 #If someone in your dataset is identified, print their name on the screen
#                 #if currentname != name:
#                 #	currentname = name
#                 #	print(currentname)
#                 #else:
#                 #	currentname = "Unknown"
#             # update the list of names
#             names.append(name)

#         # loop over the recognized faces
#         for ((top, right, bottom, left), name) in zip(boxes, names):
#             # (x, y, w, h) = [c * n // d for c, n, d in zip(f, (w0, h0) * 2, (w1, h1) * 2)]            
#             # cv2.rectangle(m.array, (x, y), (x + w, y + h), (0, 255, 0, 0))
            
#             # draw the predicted face name on the image - color is in BGR
#             cv2.rectangle(m.array, (left, top), (right, bottom),
#                 (0, 255, 225), 0)
#             y = top - 15 if top - 15 > 15 else top + 15
#             cv2.putText(m.array, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
#                 .8, (0, 255, 255), 0)
				
# def get_footage():
#     global boxes
#     global names
#     global encodings
#     global unknown_num
    
#     picam2.post_callback = draw_faces
#     picam2.start(show_preview = True)
#     # loop over frames from the video file stream
#     while True:
#         # grab the frame from the threaded video stream and resize it
#         # to 500px (to speedup processing)
#         frame = picam2.capture_array()
#         rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         # Detect the fce boxes
#         boxes = face_recognition.face_locations(rgb)
#         # compute the facial embeddings for each face bounding box
#         encodings = face_recognition.face_encodings(rgb, boxes)
#         names = []

#         # Encode the frame in JPEG format
#         _, buffer = cv2.imencode('.jpg', rgb)
#         web_frame = buffer.tobytes()
        
#         yield (b'--web_frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#         #if keyboard.is_pressed('q'):
#         #	break
#         # display the image to our screen
#         #cv2.imshow("Facial Detection", frame)
#         #key = cv2.waitKey(1)# & 0xFF
#         #if key%256 == 27:
#         #	break
#         # quit when 'q' key is pressed
#         #if key == ord("q"):
#         #	break


#     # do a bit of cleanup
#     cv2.destroyAllWindows()
#     picam2.stop_preview()
#     picam2.stop()

    

