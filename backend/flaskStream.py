#! /usr/bin/python

# import the necessary packages
#from picamera2 import Picamera2, MappedArray, Preview
import numpy as np
from imutils import paths
import os
import threading
#import queue
#import face_recognition
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
unknown_dir = 'frontend/static/faceImages'
dictEncodingStr = "encodings"
dictNamesStr = "names"
encoding_dict = {dictEncodingStr: [], dictNamesStr: []}
unknown_dict: dict[list, StreamTimer] = {}
unknown_num = 0
UNKNOWN_BUFFER_TIME = 3.0
UNKNOWN_DETECTIONS_ALLOWED = 1
faces: list[Face] = []
boxes = []
encodings = []
names = []
rgb = np.array([])
face_annotations = np.array([])
camera_inited = False
recognition_thread = None
thread_processing = False
lock_face_annotations = False


@stream.route('/stream', methods=['GET'])
@login_required
def show():
    form = CSRFForm()
    load_face_encodings()
    return render_template('stream.html', title='ShockerSecurity', form=form)


@stream.route('/stream/security_footage')
@login_required  # Protect the video feed route
def stream_footage():
    #return Response(stream_with_context(get_footage()), mimetype='multipart/x-mixed-replace; boundary=web_frame')
    print('test')

def load_face_encodings():
    global encoding_dict
    faces = getAllFaces()
    encoding_dict = {dictEncodingStr: [], dictNamesStr: []}
    for face in faces:
        #print(f'face path: {face.image_path}')
        encoding_dict[dictEncodingStr].append(face.encodings)
        encoding_dict[dictNamesStr].append(face.name)

# def run_face_recognition():
#     global boxes, encodings, names, thread_processing, face_annotations
#     thread_processing = True
#     while True:
#         #face_annotations = np.array([])
#         if (rgb.size == 0):
#             #print('no rgb image, waiting!')
#             continue
#         proc_frame = rgb.copy()
#         # Detect the face boxes
#         boxes = face_recognition.face_locations(proc_frame)
#         # compute the facial embeddings for each face bounding box
#         encodings = face_recognition.face_encodings(proc_frame, boxes)
#         names = []
#         #print(f'encoding_dict: {encoding_dict[dictEncodingStr]}')
#         #print(f'encoding matches: {matches}')
#         # loop over the facial embeddings
#         for encoding in encodings:
#             matches = face_recognition.compare_faces(encoding_dict[dictEncodingStr], encoding)
#             name = ''
            
#             if not any(matches): # if all values are False  #len(matches) == 0:
#                 # No matches found; we now need to compare against unknown_dict
#                 found_similar = False
#                 # Check against the existing encodings in unknown_dict
#                 for tuple_encoding in unknown_dict.keys():
#                     unknown_encoding = np.array(tuple_encoding)
#                     if face_recognition.compare_faces([unknown_encoding], encoding)[0]:
#                         found_similar = True
#                         unknown_dict[tuple_encoding].iterate_detected()
#                         if unknown_dict[tuple_encoding].get_times_detected() > UNKNOWN_DETECTIONS_ALLOWED or unknown_dict[tuple_encoding].time_left() < 0.5:
#                             check_unknown_alert(tuple_encoding)
#                         break
#                 if not found_similar:
#                     encoding_tuple = tuple(encoding)
#                     unknown_dict[encoding_tuple] = StreamTimer(UNKNOWN_BUFFER_TIME, check_unknown_alert, args=[encoding_tuple])
#                     unknown_dict[encoding_tuple].iterate_detected()
#                     unknown_dict[encoding_tuple].start()
#                 name = 'Unknown!'
#             else:
#                 # find the indexes of all matched faces then initialize a
#                 # dictionary to count the total number of times each face
#                 # was matched
#                 matchedIdxs = [i for (i, b) in enumerate(matches) if b]
#                 counts = {}

#                 # loop over the matched indexes and maintain a count for
#                 # each recognized face face
#                 for i in matchedIdxs:
#                     name = encoding_dict[dictNamesStr][i]
#                     counts[name] = counts.get(name, 0) + 1

#                 #print(f'matches found: {matches}')
#                 #print(f'counts found: {counts}')

#                 # determine the recognized face with the largest number
#                 # of votes (note: in the event of an unlikely tie Python
#                 # will select first entry in the dictionary)
#                 name = max(counts, key=counts.get)
#                 #print(f'detected face: {name}!')
#             # update the list of names
#             names.append(name)
#         if len(names) > 0:
#             # Create a transparent RGBA image with the same dimensions as the original
#             face_annotations = np.zeros((proc_frame.shape[0], proc_frame.shape[1], 4), dtype=np.uint8)
#             #face_annotations = #np.zeros_like(proc_frame.array) #np.zeros(proc_frame.shape, dtype=np.uint8)# # Black frame with same size as original
#         else:
#             face_annotations = np.array([])
        
#         # loop over the recognized faces
#         for ((top, right, bottom, left), name) in zip(boxes, names):
#             # (x, y, w, h) = [c * n // d for c, n, d in zip(f, (w0, h0) * 2, (w1, h1) * 2)]            
#             # cv2.rectangle(m.array, (x, y), (x + w, y + h), (0, 255, 0, 0))
            
#             # draw the predicted face box on the image - color is in BGR
#             cv2.rectangle(face_annotations, (left, top), (right, bottom), (0, 255, 225), 2)
#             # draw the predicted face name on the image - color is in BGR
#             y = top - 15 if top - 15 > 15 else top + 15
#             cv2.putText(face_annotations, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        
#     thread_processing = False

# # def draw_faces(request):
#     # global unknown_num, unknown_dict, face_annotations
#     # global boxes, encodings, names#, rgb
#     # with MappedArray(request, "main") as m:
        
#         # # Clear the annotated_frame and start fresh
#         # #print(f"m.array shape: {m.array.shape}") #returns "(480, 640, 4)"
#         # face_annotations = np.zeros_like(m.array)  # Black frame with same size as original
#         # name = ''
#         # # loop over the facial embeddings
#         # for encoding in encodings:
#             # matches = face_recognition.compare_faces(encoding_dict[dictEncodingStr], encoding)
#             # if matches is None:
#                 # # No matches found; we now need to compare against unknown_dict
#                 # found_similar = False
#                 # # Check against the existing encodings in unknown_dict
#                 # for unknown_encoding in unknown_dict.keys():
#                     # if face_recognition.compare_faces([unknown_encoding], encoding)[0]:
#                         # found_similar = True
#                         # unknown_dict[unknown_encoding].iterate_detected()
#                         # if unknown_dict[unknown_encoding].get_times_detected() > UNKNOWN_DETECTIONS_ALLOWED or unknown_dict[unknown_encoding].time_left < 0.5:
#                             # check_unknowrgb_with_alpha,n_alert(unknown_encoding)
#                         # break
#                 # if not found_similar:
#                     # unknown_dict[encoding] = StreamTimer(UNKNOWN_BUFFER_TIME, check_unknown_alert, args=[encoding])
#                     # unknown_dict[encoding].iterate_detected()
#                     # unknown_dict[encoding].start()
#                 # name = 'Unknown!'
#             # else:
#                 # # find the indexes of all matched faces then initialize a
#                 # # dictionary to count the total number of times each face
#                 # # was matched
#                 # matchedIdxs = [i for (i, b) in enumerate(matches) if b]
#                 # counts = {}

#                 # # loop over the matched indexes and maintain a count for
#                 # # each recognized face face
#                 # for i in matchedIdxs:
#                     # name = encoding_dict[dictNamesStr][i]
#                     # counts[name] = counts.get(name, 0) + 1

#                 # # determine the recognized face with the largest number
#                 # # of votes (note: in the event of an unlikely tie Python
#                 # # will select first entry in the dictionary)
#                 # name = max(counts, key=counts.get)
#             # # update the list of names
#             # names.append(name)

#         # # loop over the recognized faces
#         # for ((top, right, bottom, left), name) in zip(boxes, names):
#             # # (x, y, w, h) = [c * n // d for c, n, d in zip(f, (w0, h0) * 2, (w1, h1) * 2)]            
#             # # cv2.rectangle(m.array, (x, y), (x + w, y + h), (0, 255, 0, 0))
            
#             # # draw the predicted face box on the image - color is in BGR
#             # cv2.rectangle(face_annotations, (left, top), (right, bottom), (0, 255, 225), 0)
#             # # draw the predicted face name on the image - color is in BGR
#             # y = top - 15 if top - 15 > 15 else top + 15
#             # cv2.putText(face_annotations, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 0)
				
# def check_unknown_alert(unknown_encoding):
#     global unknown_dict, unknown_num
#     if unknown_dict[unknown_encoding].time_left() != 0: #add to db bc alerted before timer ending
#         unknown_dict[unknown_encoding].cancel()
#         face_name = "face_{0}.jpg".format(unknown_num)
#         face_path = "{0}/{1}".format(unknown_dir, face_name)
#         cv2.imwrite(face_path, rgb)
#         #print(f'tuple ver: {unknown_encoding}.\nconverted back: {np.array(unknown_encoding)}')

#         addFace('Unknown!', False, face_name, np.array(unknown_encoding))
#         print("unknown face detected! Send picture to user!")
#         #print("unknown num: {}".format(unknown_num))
#         unknown_num += 1
#         load_face_encodings() #added new face so reload encodings
#     else: #timer finished before registering
#         print('face not detected again before timer timeout!')
#     # either way remove from dict
#     unknown_dict.pop(unknown_encoding)
    
#     # has_unknown = False
#     # for encoding in encodings:
#     #     matches = face_recognition.compare_faces(unknown_encoding, encoding)
#     #     if any(matches):  # checks if there are matches
#     #         has_unknown = True
#     #         break
#     # if has_unknown:
        
    
        
        
            
# def get_footage():
#     global boxes
#     global names
#     global encodings
#     global rgb
#     global face_annotations
    
#     # picam2.post_callback = draw_faces
#     # picam2.start()#(show_preview = True)
    
#     # loop over frames from the video file stream
#     while True:
#         # grab the frame from the threaded video stream and resize it
#         # to 500px (to speedup processing)
#         frame = picam2.capture_array()
#         rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
#         #rgb = cv2.cvtColor(m.array, cv2.COLOR_BGR2RGB)
#         # # Detect the face boxes
#         # boxes = face_recognition.face_locations(rgb)
#         # # compute the facial embeddings for each face bounding box
#         # encodings = face_recognition.face_encodings(rgb, boxes)
#         # names = []
        
#         #Display the image (for debugging)
#         #cv2.imshow("rgb Frame", rgb)
#         annotated_frame = rgb.copy()
#         if face_annotations.size != 0:
#             copy_annotations = face_annotations.copy()
#             #print(f'have face annotations!')
           
#             # Convert the original BGR image to RGBA (so we can blend it with the annotations)
#             rgb_with_alpha = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2BGRA)
            
#             if copy_annotations.size == 0:
#                 print('somehow annotations zero size boooohoooo')
#                 continue
#             # Blend the annotations onto the original image using `cv2.addWeighted`
#             # The alpha channel in `face_annotations` will control transparency
#             annotated_frame = cv2.addWeighted(rgb_with_alpha, 1, copy_annotations, 1, 0)
            
#             # Convert back to BGR if you want to display it or save it in BGR format
#             #annotated_frame = cv2.cvtColor(alpha_annotated_frame, cv2.COLOR_BGRA2BGR)

#         # Set the JPEG compression quality to a lower value (e.g., 75)
#         encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]  # 75 is lower quality
#         # Encode the frame in JPEG format
#         _, buffer = cv2.imencode('.jpg', annotated_frame, encode_param)
#         web_frame = buffer.tobytes()
        
#         #print('yielding web frame!')
#         yield (b'--web_frame\r\n'
#             b'Content-Type: image/jpeg\r\n\r\n' + web_frame + b'\r\n')

def init_video():
    global picam2, unknown_num, camera_inited, recognition_thread, face_annotations
    load_face_encodings()
    # unknown_num = len(list(paths.list_images(unknown_dir))) + 1
    # print("unknown num: {}".format(unknown_num))

    # picam2 = Picamera2()
    # picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480),}))#, lores={"size": (320, 240), "format": "YUV420"}))
    # #picam2.post_callback = draw_faces
    # #picam2.start_preview(Preview.QTGL, width=640, height=480)
    # #dest_dir = "MemberVideo"
    # #picam2.start_and_record_video("memberVideo.mp4", duration=5)

    # (w0, h0) = picam2.stream_configuration("main")["size"] 
    # #(w1, h1) = picam2.stream_configuration("lores")["size"]
    
    # picam2.start()#show_preview = True)
    # camera_inited = True
    # face_annotations = np.array([])
    # # Start the face recognition thread (only once)
    # if not thread_processing:  # Ensure we only start one thread
    #     recognition_thread = threading.Thread(target=run_face_recognition, daemon=True)
    #     recognition_thread.start()
        
def stop_video():
    global picam2, thread_processing
    picam2.stop()
    if thread_processing:
        recognition_thread.stop()
        thread_processing = False


    

