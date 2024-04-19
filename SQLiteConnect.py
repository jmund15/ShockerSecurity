import sqlite3 

def convertToBinaryData(filename): 
	with open(filename, 'rb') as file: 
		blobData = file.read() 
	return blobData 

def insertBLOB(name, photo): 
	try: 
		sqliteConnection = sqlite3.connect('ShockerSecurity.db') 
		cursor = sqliteConnection.cursor() 
		print("Connected to SQLite") 
		
		sqlite_insert_blob_query = """ INSERT INTO AcceptedFaces (Name, IMG) VALUES (?, ?)"""
		
		empPhoto = convertToBinaryData(photo) 
		
		cursor.execute(sqlite_insert_blob_query, (name, empPhoto,)) 
		sqliteConnection.commit() 
		print("Image and file inserted successfully as a BLOB into a table") 
		cursor.close() 

	except sqlite3.Error as error: 
		print("Failed to insert data into sqlite table", error) 
	
	finally: 
		if sqliteConnection: 
			sqliteConnection.close() 

def convertToImage(blobData, filename):
    with open(filename, 'wb') as file:
        file.write(blobData)

def dbConnect():
    sqliteConnection = sqlite3.connect('ShockerSecurity.db')
    cursor = sqliteConnection.cursor()
    table = """ CREATE TABLE IF NOT EXISTS AcceptedFaces (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
            IMG BLOB
        ); """
    cursor.execute(table)
    print("Table is Ready")
    return sqliteConnection, cursor

if __name__ == '__main__':
    sqliteConnection, cursor = dbConnect()

    base_dir = os.path.abspath(os.path.dirname(__file__))
    photo_path = os.path.join(base_dir, "sample1.jpg")
    
    insertBLOB("Sarah", photo_path) 
    
    statement = '''SELECT * FROM AcceptedFaces'''
    cursor.execute(statement) 
    print("Data: ") 
    output = cursor.fetchall() 
    for row in output: 
        print(row) 
    
    sqliteConnection.commit() 
    sqliteConnection.close()
