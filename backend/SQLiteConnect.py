import sqlite3
import os
import inspect
from cryptography.fernet import Fernet
from werkzeug.security import generate_password_hash, check_password_hash

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
    addFace('Kyle', True, "Kyle\image_0.jpg", 'testencodings2')
    
        


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
def getAllFaces() -> list[Face]:
    statement = '''SELECT * FROM faces'''
    faces = []
    try:
        # Execute the statement
        curs.execute(statement)
        rows = curs.fetchall()

        # Create Face objects and append to the list
        for row in rows:
            uid, name, accepted, imgPath, encodings  = row
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

def updateFace(id, name, accepted) -> bool: #face encodings and pictures won't be updated right?
    statement = '''UPDATE Faces SET name = ?, accepted = ? WHERE id = ?'''
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

    #empPhoto = convertToBinaryData(pictureLoc)
    #encryptedPhoto = encryptData(empPhoto)
    try:
        # Execute the insert statement
        curs.execute(statement, (name, accepted, imgPath, encodings))
        # Commit the transaction
        conn.commit()
        print("Image and file inserted successfully as a BLOB into a table")
        return True
    except sqlite3.Error as e:
        print(f"{inspect.currentframe().f_code.co_name} ERROR: {e}")
        return False
    
def deleteFace(uid):
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
