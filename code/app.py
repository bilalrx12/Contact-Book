from flask import Flask 
import sqlite3
from flask_restful import Resource, Api, reqparse

app= Flask(__name__)
api= Api(app)

@app.route('/contactbook')
def home():
    return "Contact Book"


class contact_book(Resource):

    parser= reqparse.RequestParser()
    parser.add_argument('ID')
    parser.add_argument('email')
    parser.add_argument('phone')
    
    #Implement GET Method
    def get(self,name):
        entry= self.findbyname(name) #Get entry by name
        if entry:
            return entry
        return {'message': 'Entry not found'} #If no entry exist return message

    @classmethod 
    def findbyname(cls,name): #Find Entry through name
        connection=sqlite3.connect('data.db')
        cursor=connection.cursor()

        # Find entry in contact_book using name
        query = "SELECT * FROM contact_book WHERE name=?"
        result= cursor.execute(query, (name,))
        # fetch 1st entry found
        row= result.fetchone()
        connection.close()
        # if row exist return the  entry
        if row:
            return  {'contact_book_entry' : { 'ID' : row [0], 'name': row[1], 'email': row[2], 'phone': row[3]}}

    #Implement POST Method
    def post(self,name):
        # If entry already exist return message
        if self.findbyname(name):
            return {'message': "An entry with Name already exist"}

        # GET data through body of request
        data = contact_book.parser.parse_args()
        #create an entry
        entry= { 'ID': data['ID'], 'name': name, 'email': data['email'],'phone': data['phone']}

        #insert entry into database
        self.insert(entry)

        
        return entry

    #method to insert entry into database 
    @classmethod
    def insert(cls,entry):
        connection=sqlite3.connect('data.db')
        cursor=connection.cursor()

        query = "INSERT INTO contact_book VALUES (?,?,?,?)"

        cursor.execute(query,(entry['ID'], entry['name'],entry['email'],entry['phone']))

        connection.commit()
        connection.close()

    #Implement PUT Method
    def put(self,name):
        # GET data through body of request
        data = contact_book.parser.parse_args()

        # create a new entry by find the old entry
        entry=self.findbyname(name)
        entry_update={ 'ID': data['ID'], 'name': name, 'email': data['email'],'phone': data['phone']}

        # If entry does not exist insert a new entry. If entry exist update the entry with new entry created
        if entry is None:
            self.insert(entry_update)
        else: 
            self.update(entry_update)
        
        return entry_update

    # method to update entry into data base  
    @classmethod
    def update(cls,entry):
        connection=sqlite3.connect('data.db')
        cursor=connection.cursor()
        query = "UPDATE contact_book SET ID=?, email=?, phone=? WHERE name=?"
        cursor.execute(query, (entry['ID'],entry['email'],entry['phone'],entry['name']))

        connection.commit()
        connection.close()

    
    #Implement DELETE Method
    def delete(self,name):

        #Delete entry from database
        connection=sqlite3.connect('data.db')
        cursor=connection.cursor()
        query = "DELETE FROM contact_book WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return{'message': 'Entry deleted'}


# Class to retrieve all entries in database
class contactbookentries(Resource):
    def get(self):

        #select all entries and append them to an entries variable 
        connection = sqlite3.connect('data.db')
        cursor=connection.cursor()

        query ="SELECT * FROM contact_book"
        result= cursor.execute(query)
        print(result)
        entries =[]
        for row in result:
            entries.append({'ID':row[0],'name': row[1],'email': row[2], 'phone': row[3]})
        
        connection.close()
        return entries

# Add resources to the API
api.add_resource(contact_book,'/contactbook/<string:name>')
api.add_resource(contactbookentries,'/contactbookentries')

# run the app
if __name__== "__main__":
    app.run(port=5000, debug=True)