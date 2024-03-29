import sqlite3 

def convertToBinaryData(filename): 
	with open(filename, 'rb') as file: 
		blobData = file.read() 
	return blobData 

def insertBLOB(photo): 
	try: 
		sqliteConnection = sqlite3.connect('ShockerSecurity.db') 
		cursor = sqliteConnection.cursor() 
		print("Connected to SQLite") 
		
		sqlite_insert_blob_query = """ INSERT INTO AcceptedFaces (IMG) VALUES (?)"""
		
		empPhoto = convertToBinaryData(photo) 
		
		cursor.execute(sqlite_insert_blob_query, (empPhoto,)) 
		sqliteConnection.commit() 
		print("Image and file inserted successfully as a BLOB into a table") 
		cursor.close() 

	except sqlite3.Error as error: 
		print("Failed to insert blob data into sqlite table", error) 
	
	finally: 
		if sqliteConnection: 
			sqliteConnection.close() 



sqliteConnection = sqlite3.connect('ShockerSecurity.db')
cursor = sqliteConnection.cursor()

cursor.execute("DROP TABLE IF EXISTS AcceptedFaces")

table = """ CREATE TABLE AcceptedFaces (
			ID INTEGER PRIMARY KEY AUTOINCREMENT,
            IMG BLB
		); """

cursor.execute(table)
print("Table is Ready")

insertBLOB("C:\Temp\ShockerSecurity\sample1.jpg") 

statement = '''SELECT * FROM AcceptedFaces'''

cursor.execute(statement) 

print("Data: ") 
output = cursor.fetchall() 
for row in output: 
    print(row) 

sqliteConnection.commit() 
sqliteConnection.close()