import sqlite3
import numpy as np
import os
import inspect
from cryptography.fernet import Fernet
from werkzeug.security import generate_password_hash, check_password_hash
#from face_recognition import compare_faces

from flaskModels import User, Face

DATABASE = 'backend/ShockerSecurity.db'
# conn = sqlite3.connect(DATABASE)
# curs = conn.cursor()
# Initialize to None at the module level
conn = None
curs = None
key = None
cipher = None

def initialize_db():
    global conn, curs  # Use global to modify the module-level variables
    if conn is None or curs is None:  # Check if they are already initialized
        conn = sqlite3.connect(DATABASE, check_same_thread=False) #BAD!
        curs = conn.cursor()
    
    global key, cipher
    key = Fernet.generate_key()
    cipher = Fernet(key)
    
    #addUser('wiispeed03@gmail.com', 'testPassword')
    #addFace('Kyle', True, "Kyle\image_1.jpg", 'testencodings2')
    #addFace('Lorant', True, "Lorant\image_0.jpg", 'testencodings3')
    #addFace('Tina', True, "Tina\image_1.jpg", 'testencodings4')
        
def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def encryptData(data):
    return cipher.encrypt(data)

def decryptData(data):
    return cipher.decrypt(data)

def addUser(email, password):
    # Prepare the SQL insert statement
    statement = '''INSERT INTO users (email, password) VALUES (?, ?)'''
    # Hash the password before storing
    hashed_password = generate_password_hash(password)#, method='sha256')
    try:
        # Execute the insert statement
        curs.execute(statement, (email, hashed_password))
        # Commit the transaction
        conn.commit()
        print("Admin user added successfully.")
        return True
    except sqlite3.Error as e:
        print(f"{inspect.currentframe().f_code.co_name} ERROR: {e}")
        return False
    
def getIdFromEmail(email):
    print('email provided: ', email)
    statement = '''SELECT uid FROM users WHERE email = ?'''
    try:
        curs.execute(statement, (email,))
        result = curs.fetchone()
        if result:
            return result[0]  # (uid, email, password)
        else:
            return None #'Unknown Error!' # should be impossible  
    except sqlite3.Error as e:
        print(f"{inspect.currentframe().f_code.co_name} ERROR: {e}")
        return None
    
def getUserFromID(id):
    print('uid provided: ', id)
    statement = '''SELECT * FROM users WHERE uid = ?'''
    try:
        curs.execute(statement, (id,))
        result = curs.fetchone()
        if result:
            return User(result[0], result[1], result[2])  # (uid, email, password)
        else:
            return None #'Unknown Error!' # should be impossible  
    except sqlite3.Error as e:
        print(f"{inspect.currentframe().f_code.co_name} ERROR: {e}")
        return None
    
def validateUser(email, password):
    stored_password_statement = '''SELECT password FROM users WHERE email = ?'''
    try:
        curs.execute(stored_password_statement, (email,))
        result = curs.fetchone()
        if result : #user exists 
            hashed_password = result[0]
            if not check_password_hash(hashed_password, password):
                return None #'Incorrect Password!'  
            statement = '''SELECT * FROM users WHERE email = ? AND password = ?'''
            curs.execute(statement, (email, hashed_password))
            result = curs.fetchone()
            if result:
                # User exists; return all fields
                return User(result[0], result[1], result[2])  # (uid, email, password)
            else:
                return None #'Unknown Error!' # should be impossible  
        else:
            return None #'Incorrect Email!'
    except sqlite3.Error as e:
        print(f"'checkUser' ERROR: {e}")
        return None
    
def get_unique_face_name(base_name):
    name = base_name
    i = 1
    
    while True:
        # Check if the name already exists
        curs.execute("SELECT COUNT(*) FROM faces WHERE name = ?", (name,))
        count = curs.fetchone()[0]
        
        if count == 0:
            break  # Unique name found
        else:
            # Increment the name
            name = f"{base_name}{i}"
            i += 1
    
    return name
    
def getFaceFromName(name) -> Face:
    statement = '''SELECT * FROM faces WHERE name = ?'''
    try:
        # Execute the statement
        curs.execute(statement, (name,))
        result = curs.fetchone()
        
        #print('getFaceFromName result: ', result)
        
        if result:
            return Face(result[0], result[1], result[2], result[4], result[3])
        else:
            return None # face not found
    except sqlite3.Error as e:
        print(f"'getFaceFromName' ERROR: {e}")
        return None    
    
def getFaceFromEncodings(encodings) -> Face:
    statement = '''SELECT * FROM faces WHERE encodings = ?'''
    try:
        # Execute the statement
        curs.execute(statement, (encodings,))
        result = curs.fetchone()

        if result:
            return Face(result[0], result[1], result[2], result[4], result[3])
        else:
            return None # face not found
    except sqlite3.Error as e:
        print(f"'getFaceFromEncodings' ERROR: {e}")
        return None
    
def getAllFaces() -> list[Face]:
    statement = '''SELECT * FROM faces'''
    faces = []
    try:
        # Execute the statement
        curs.execute(statement)
        rows = curs.fetchall()

        # Create Face objects and append to the list
        for row in rows:
            uid, name, accepted, imgPath, blob_encodings  = row
            encodings = np.frombuffer(blob_encodings, dtype=np.float64) 
            print('face imgPath: ', imgPath)
            #decryptedBlob = decryptData(blob)
            face = Face(uid, name, accepted, encodings, imgPath)
            faces.append(face)
    except sqlite3.Error as e:
        print(f"'getAllFaces' ERROR: {e}")
    return faces

def getAllFacesRaw() -> list[any]:
    statement = '''SELECT * FROM faces'''
    faces = []
    try:
        # Execute the statement
        curs.execute(statement)
        faces = curs.fetchall()
    except sqlite3.Error as e:
        print(f"'getAllFaces' ERROR: {e}")
    return faces

def matchEncodings(matchEncoding):
    old_statement = '''SELECT name FROM faces WHERE encodings = ?'''
    statement = '''SELECT encodings FROM faces'''
    try:
        curs.execute(statement)
        encodings = curs.fetchall()
        # for encoding in encodings:
        #     matches = face_recognition.compare_faces(encoding,
        #         matchEncoding)
        #     # check to see if we have found a match
        #     if True in matches:
        #         name_statement = '''SELECT name FROM faces WHERE encodings = ?'''
        #         curs.execute(name_statement, (encoding,))
        #         result = curs.fetchone()
        #         if result:
        #             return matches, result[0]  # (uid, email, password)
        #         else:
        #             return None #'Unknown Error!' # should be impossible 
    except sqlite3.Error as e:
        print(f"{inspect.currentframe().f_code.co_name} ERROR: {e}")
        return None

def updateFace(id, name, accepted) -> bool: #face encodings and pictures won't be updated right?
    statement = '''UPDATE Faces SET name = ?, accepted = ? WHERE uid = ?'''
    try:
        # Execute the update statement and commit changes
        curs.execute(statement, (name, accepted, id))
        conn.commit()
        # Check if any rows were affected
        if curs.rowcount > 0:
            print("Face updated successfully.")
        else:
            print(f"No face found with id {id}.")
            return False
        return True
    except sqlite3.Error as e:
        print(f"{inspect.currentframe().f_code.co_name} ERROR: {e}")
        return False

def addFace(name, accepted, imgPath, encodings):
    statement = ''' INSERT INTO faces (name, accepted, imgPath, encodings) VALUES (?, ?, ?, ?)'''

    get_unique_face_name(name)
    #empPhoto = convertToBinaryData(pictureLoc)
    #encryptedPhoto = encryptData(empPhoto)
    
    #convert encodings to bytes
    blob_encodings = encodings.tobytes()
    try:
        # Execute the insert statement
        curs.execute(statement, (name, accepted, imgPath, blob_encodings))
        # Commit the transaction
        conn.commit()
        print("Image and file inserted successfully as a BLOB into a table")
        return True
    except sqlite3.Error as e:
        print(f"{inspect.currentframe().f_code.co_name} ERROR: {e}")
        return False
    
def deleteFace(uid):
    print('deleteFace called')
    # Prepare the DELETE statement
    statement = '''DELETE FROM faces WHERE uid = ?'''
    try:
        # Execute the statement and commit changes
        curs.execute(statement, (uid,))
        conn.commit()
        
        # Check if any row was deleted
        if curs.rowcount > 0:
            print(f"Face with uid {uid} has been removed.")
        else:
            print(f"No face found with uid {uid}.")
            return False
        return True
    except sqlite3.Error as e:
        print(f"{inspect.currentframe().f_code.co_name} ERROR: {e}")
        return False

def getAllEmails() -> list[str]:
    statement = '''SELECT email FROM users'''
    emails = []
    try:
        # Execute the statement
        curs.execute(statement)
        rows = curs.fetchall()

        # Extract emails and add them to the list
        emails = [row[0] for row in rows]
    except sqlite3.Error as e:
        print(f"'getAllEmails' ERROR: {e}")
    return emails

def insertBLOB(name, photo):
    try:
        sqliteConnection = sqlite3.connect(DATABASE)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_blob_query = """ INSERT INTO AcceptedFaces (Name, IMG) VALUES (?, ?)"""

        empPhoto = convertToBinaryData(photo)
        encryptedPhoto = encryptData(empPhoto)

        cursor.execute(sqlite_insert_blob_query, (name, encryptedPhoto,))
        sqliteConnection.commit()
        print("Image and file inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()

def convertToImage(blobData, filename):
    decryptedData = decryptData(blobData)
    with open(filename, 'wb') as file:
        file.write(decryptedData)

def dbConnect():
    sqliteConnection = sqlite3.connect(DATABASE)
    cursor = sqliteConnection.cursor()
    # table = """ CREATE TABLE IF NOT EXISTS AcceptedFaces (
    #     ID INTEGER PRIMARY KEY AUTOINCREMENT,
    #     Name TEXT,
    #     IMG BLOB
    # ); """
    # cursor.execute(table)
    # print("Table is Ready")
    return sqliteConnection, cursor

# if __name__ == '__main__':
#     conn, curs = dbConnect()

#     base_dir = os.path.abspath(os.path.dirname(__file__))
#     photo_path = os.path.join(base_dir, "sample1.jpg") 

#     insertBLOB("Sarah", photo_path)

#     statement = '''SELECT * FROM AcceptedFaces'''
#     curs.execute(statement)
#     print("Data: ")
#     output = curs.fetchall()
#     for row in output:
#         print(row)

#     conn.commit()
#     conn.close()
