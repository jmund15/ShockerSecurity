#! /usr/bin/python

# import the necessary packages
from picamera2 import Picamera2, MappedArray, Preview
import numpy as np
from imutils import paths
import os
import threading
import face_recognition
import imutils
import time 
from flask import Blueprint, Response, render_template, stream_with_context
from flask_login import login_required

import time
import numpy as np
import cv2

from flaskModels import Face, CSRFForm
from SQLiteConnect import addFace, getAllFaces

stream = Blueprint('stream', __name__, template_folder='../frontend')

face_dir = 'frontend/static'
dictEncodingStr = "encodings"
dictNamesStr = "names"
encoding_dict = {dictEncodingStr: [], dictNamesStr: []}
unknown_dict: dict[list, threading.Timer] = {}
UNKNOWN_ALERT_TIME = 2.0
faces: list[Face] = []
boxes = []
encodings = []
names = []
unknown_num = len(list(paths.list_images(face_dir))) + 1 #TODO: FIX!
print("unknown num: {}".format(unknown_num))
rgb = None
face_annotations = None

def init_video():
    load_face_encodings()

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
    dest_dir = "MemberVideo"
    #picam2.start_and_record_video("memberVideo.mp4", duration=5)

    (w0, h0) = picam2.stream_configuration("main")["size"] 
    #(w1, h1) = picam2.stream_configuration("lores")["size"]


@stream.route('/stream', methods=['GET'])
@login_required
def show():
    form = CSRFForm()
    #print('STREAMING HTML LOAD!')
    return render_template('stream.html', title='ShockerSecurity', form=form)


@stream.route('/stream/security_footage')
@login_required  # Protect the video feed route
def stream_footage():
    return Response(stream_with_context(get_footage()), mimetype='multipart/x-mixed-replace; boundary=frame')

def load_face_encodings():
    global encoding_dict
    faces = getAllFaces()
    encoding_dict = {dictEncodingStr: [], dictNamesStr: []}
    for face in faces:
        encoding_dict[dictEncodingStr].append(face.encodings)
        encoding_dict[dictNamesStr].append(face.name)


def draw_faces(request):
    global unknown_num, unknown_dict, names, face_annotations
    
    with MappedArray(request, "main") as m:
        # Clear the annotated_frame and start fresh
        face_annotations = np.zeros_like(m.array)  # Black frame with same size as original
        
        # loop over the facial embeddings
        for encoding in encodings:
            matches = face_recognition.compare_faces(encoding_dict[dictEncodingStr], encoding)
            if matches is None:
                if encoding not in unknown_dict:
                    unknown_dict[encoding] = threading.Timer(UNKNOWN_ALERT_TIME, check_unknown_alert, args=[encoding])
                    unknown_dict[encoding].start()
            else:
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for i in matchedIdxs:
                    name = encoding_dict[dictNamesStr][i]
                    counts[name] = counts.get(name, 0) + 1

                # determine the recognized face with the largest number
                # of votes (note: in the event of an unlikely tie Python
                # will select first entry in the dictionary)
                name = max(counts, key=counts.get)
            # update the list of names
            names.append(name)

        # loop over the recognized faces
        for ((top, right, bottom, left), name) in zip(boxes, names):
            # (x, y, w, h) = [c * n // d for c, n, d in zip(f, (w0, h0) * 2, (w1, h1) * 2)]            
            # cv2.rectangle(m.array, (x, y), (x + w, y + h), (0, 255, 0, 0))
            
            # draw the predicted face name on the image - color is in BGR
            cv2.rectangle(face_annotations, (left, top), (right, bottom), (0, 255, 225), 0)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(face_annotations, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 0)
				
def check_unknown_alert(unknown_encoding):
    global encodings
    has_unknown = False
    for encoding in encodings:
        matches = face_recognition.compare_faces(unknown_encoding, encoding)
        if any(matches):  # checks if there are matches
            has_unknown = True
            break
    if has_unknown:
        cv2.imwrite("{0}/unknown_{1}.jpg".format(face_dir, unknown_num), rgb)
        addFace('Unknown', False, '', unknown_encoding)
        print("unknown face detected! Send picture to user!")
        print("unknown num: {}".format(unknown_num))
        unknown_num += 1
        load_face_encodings() #added new face so reload encodings
    # else false alarm
    unknown_dict.pop(unknown_encoding)
        
        
            
def get_footage():
    global boxes
    global names
    global encodings
    global unknown_num
    global rgb
    
    picam2.post_callback = draw_faces
    picam2.start(show_preview = True)
    # loop over frames from the video file stream
    while True:
        # grab the frame from the threaded video stream and resize it
        # to 500px (to speedup processing)
        frame = picam2.capture_array()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        annotated_frame = rgb
        if face_annotations is not None:
            annotated_frame = cv2.addWeighted(annotated_frame, 1, face_annotations, 1, 0)
        # Detect the face boxes
        boxes = face_recognition.face_locations(rgb)
        # compute the facial embeddings for each face bounding box
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []

        # Encode the frame in JPEG format
        _, buffer = cv2.imencode('.jpg', annotated_frame)
        web_frame = buffer.tobytes()
        
        yield (b'--web_frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + web_frame + b'\r\n')

    

