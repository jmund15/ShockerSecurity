import numpy
import face_recognition
import os
from imutils import paths
import pickle

def encode_faces(source_dir, target_dir, name):
    print("Encoding for {}'s face".format(name))

    # initialize the list of known encodings and known names
    knownEncodings = []
    knownNames = []
    imagePaths = list(paths.list_images(source_dir))

    # loop over the image paths
    for (i, imagePath) in enumerate(imagePaths):
        # extract the person name from the image path
        #print("[INFO] processing image {}/{}".format(i + 1,
        #    len(imagePaths)))
        #name = imagePath.split(os.path.sep)[-2]

        image = face_recognition.load_image_file(imagePath)

        # detect the (x, y)-coordinates of the bounding boxes
        # corresponding to each face in the input image
        #boxes = face_recognition.face_locations(rgb, model="hog")

        # compute the facial embedding for the face
        encodings = face_recognition.face_encodings(image)

        # loop over the encodings
        for encoding in encodings:
            # add each encoding + name to our set of known names and
            # encodings
            knownEncodings.append(encoding)
            knownNames.append(name)

    # dump the facial encodings + names to disk
    print("[INFO] serializing encodings...")
    data = {"encodings": knownEncodings, "names": knownNames}
    pickle_name = target_dir + "/" + name + ".pickle"
    if (not os.path.isfile(pickle_name)):
        print("pickle file doesn't exist, creating it now...")
    with open(pickle_name, 'ab+') as fp:
        fp.write(pickle.dumps(data))
    #f = open(pickle_name, "wb")
    #f.write(pickle.dumps(data))
    #pickles = pickle.load(target_dir + "/encodings.pickle")
    #f.close()
    
    #self.save_array(numpy.array(knownEncodings), image_file_name = knownNames)
    print('Finished encoding', name)


def initalize_encodings(dir):
    encodings = []
    for files in os.listdir(dir):
        FNAME  = files.split('.')[0]
        encodings.append(
            {FNAME : numpy.load(dir+'/'+files)}
        )
    return encodings
