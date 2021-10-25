import sqlite3

connection = sqlite3.connect('data.db') #open connection

cursor = connection.cursor()

# Create empty table called contact_book
create_Table = "CREATE TABLE contact_book (ID int, name text, email text, phone int)"
cursor.execute(create_Table)

connection.commit() # commit changes

connection.close() # close connection
