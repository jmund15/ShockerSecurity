import pickle

from SQLiteConnect import initialize_db, getAllFaces

def load_face_encodings():
    faces = getAllFaces()
    encodingDict = {"encodings": [], "names": []}
    for face in faces:
        encodingDict["encodings"].append(face.encodings)
        encodingDict["names"].append(face.name)
    return encodingDict
       
       
       
# face = pickle.loads(open('KnownFaces\Jacob.pickle', "rb").read())
# for key, value in face.items():
#     print('key: ', key)
#     #print('value: ', value)
#     print('\n\n\n')

initialize_db()
print(load_face_encodings())
            
