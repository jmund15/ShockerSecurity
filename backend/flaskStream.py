#! /usr/bin/python

# import the necessary packages
from picamera2 import Picamera2, MappedArray, Preview
import numpy as np
from imutils import paths
import os
import face_recognition
import imutils
import time 
from flask import Blueprint, Response, render_template, stream_with_context
from flask_login import login_required

import time
import numpy as np
import cv2

from flaskModels import Face, CSRFForm, StreamTimer
from SQLiteConnect import addFace, getAllFaces

stream = Blueprint('stream', __name__, template_folder='../frontend')

picam2 = None
face_dir = 'frontend/static/faceImages'
unknown_dir = 'frontend/static/faceImages/Unknown'
dictEncodingStr = "encodings"
dictNamesStr = "names"
encoding_dict = {dictEncodingStr: [], dictNamesStr: []}
unknown_dict: dict[list, StreamTimer] = {}
unknown_num = 0
UNKNOWN_BUFFER_TIME = 2.0
UNKNOWN_DETECTIONS_ALLOWED = 2
faces: list[Face] = []
boxes = []
encodings = []
names = []
rgb = None
face_annotations = None
camera_inited = False


@stream.route('/stream', methods=['GET'])
@login_required
def show():
    form = CSRFForm()
    return render_template('stream.html', title='ShockerSecurity', form=form)


@stream.route('/stream/security_footage')
@login_required  # Protect the video feed route
def stream_footage():
    return Response(stream_with_context(get_footage()), mimetype='multipart/x-mixed-replace; boundary=web_frame')
    #print('test')

def load_face_encodings():
    global encoding_dict
    faces = getAllFaces()
    encoding_dict = {dictEncodingStr: [], dictNamesStr: []}
    for face in faces:
        encoding_dict[dictEncodingStr].append(face.encodings)
        encoding_dict[dictNamesStr].append(face.name)


def draw_faces(request):
    global unknown_num, unknown_dict, face_annotations
    global boxes, encodings, names#, rgb
    with MappedArray(request, "main") as m:
        rgb = cv2.cvtColor(m.array, cv2.COLOR_BGR2RGB)
        # Detect the face boxes
        boxes = face_recognition.face_locations(rgb)
        # compute the facial embeddings for each face bounding box
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []
        
        # Clear the annotated_frame and start fresh
        #print(f"m.array shape: {m.array.shape}") #returns "(480, 640, 4)"
        face_annotations = np.zeros_like(m.array)  # Black frame with same size as original
        name = ''
        # loop over the facial embeddings
        for encoding in encodings:
            matches = face_recognition.compare_faces(encoding_dict[dictEncodingStr], encoding)
            if matches is None:
                # No matches found; we now need to compare against unknown_dict
                found_similar = False
                # Check against the existing encodings in unknown_dict
                for unknown_encoding in unknown_dict.keys():
                    if face_recognition.compare_faces([unknown_encoding], encoding)[0]:
                        found_similar = True
                        unknown_dict[unknown_encoding].iterate_detected()
                        if unknown_dict[unknown_encoding].get_times_detected() > UNKNOWN_DETECTIONS_ALLOWED or unknown_dict[unknown_encoding].time_left < 0.5:
                            check_unknown_alert(unknown_encoding)
                        break
                if not found_similar:
                    unknown_dict[encoding] = StreamTimer(UNKNOWN_BUFFER_TIME, check_unknown_alert, args=[encoding])
                    unknown_dict[encoding].iterate_detected()
                    unknown_dict[encoding].start()
                name = 'Unknown!'
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
            
            # draw the predicted face box on the image - color is in BGR
            cv2.rectangle(face_annotations, (left, top), (right, bottom), (0, 255, 225), 0)
            # draw the predicted face name on the image - color is in BGR
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(face_annotations, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 0)
				
def check_unknown_alert(unknown_encoding):
    global unknown_dict, unknown_num
    if unknown_dict[unknown_encoding].time_left() != 0: #add to db bc alerted before timer ending
        unknown_dict[unknown_encoding].cancel()
        cv2.imwrite("{0}/unknown_{1}.jpg".format(unknown_dir, unknown_num), rgb)
        addFace('Unknown', False, '', unknown_encoding)
        print("unknown face detected! Send picture to user!")
        print("unknown num: {}".format(unknown_num))
        unknown_num += 1
        load_face_encodings() #added new face so reload encodings
    #else: #timer finished before registering
    
    # either way remove from dict
    unknown_dict.pop(unknown_encoding)
    
    # has_unknown = False
    # for encoding in encodings:
    #     matches = face_recognition.compare_faces(unknown_encoding, encoding)
    #     if any(matches):  # checks if there are matches
    #         has_unknown = True
    #         break
    # if has_unknown:
        
    
        
        
            
def get_footage():
    global boxes
    global names
    global encodings
    global rgb
    
    # picam2.post_callback = draw_faces
    # picam2.start()#(show_preview = True)
    
    # loop over frames from the video file stream
    while True:
        # grab the frame from the threaded video stream and resize it
        # to 500px (to speedup processing)
        frame = picam2.capture_array()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        
        #Display the image (for debugging)
        #cv2.imshow("rgb Frame", rgb)
        annotated_frame = rgb.copy()
        if face_annotations is not None:
            print('have face annotations!')
            cv2.imshow("annotations", face_annotations)
            face_annotations_rgb = cv2.cvtColor(face_annotations, cv2.COLOR_BGRA2RGB)
            #print(f'rgb shape & size: {annotated_frame.shape}, {annotated_frame.size}.\nannotations shape & size: {face_annotations_rgb.shape}, {face_annotations_rgb.size}')
            annotated_frame = cv2.addWeighted(annotated_frame, 1, face_annotations_rgb, 1, 0)
        
        # Display the image (for debugging)
        #cv2.imshow("Annotated Frame", annotated_frame)

        # Set the JPEG compression quality to a lower value (e.g., 75)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 75]  # 75 is lower quality
        # Encode the frame in JPEG format
        _, buffer = cv2.imencode('.jpg', rgb, encode_param)
        web_frame = buffer.tobytes()
        
        print('yielding web frame!')
        yield (b'--web_frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + web_frame + b'\r\n')

def init_video():
    global picam2, unknown_num, camera_inited
    load_face_encodings()
    unknown_num = len(list(paths.list_images(unknown_dir))) + 1
    print("unknown num: {}".format(unknown_num))

    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480),}))#, lores={"size": (320, 240), "format": "YUV420"}))
    picam2.post_callback = draw_faces
    #picam2.start_preview(Preview.QTGL, width=1280, height=960)
    #dest_dir = "MemberVideo"
    #picam2.start_and_record_video("memberVideo.mp4", duration=5)

    (w0, h0) = picam2.stream_configuration("main")["size"] 
    #(w1, h1) = picam2.stream_configuration("lores")["size"]
    
    picam2.start()
    camera_inited = True


    

