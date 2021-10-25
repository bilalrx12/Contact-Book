from app import app
import unittest
import sqlite3

entries =[]

def allentriesname():
    connection = sqlite3.connect('data.db')
    cursor=connection.cursor()
    query ="SELECT * FROM contact_book"
    result= cursor.execute(query)
    for row in result:
        entries.append(row[1])
        
    connection.close()
        

class Test(unittest.TestCase):

    # test if message returned on Homepage
    def test_index_data(self):
        tester=app.test_client(self)
        response=tester.get("/contactbook")
        print(response.data)
        self.assertTrue(b'Contact Book' in response.data)

    #test for status code
    def test_index(self):
        # Test status of entry list
        tester=app.test_client(self)
        response=tester.get("/contactbookentries")
        statuscode=response.status_code
        self.assertEqual(statuscode, 200)

        # Test status of entry book homepage
        response=tester.get("/contactbook")
        statuscode=response.status_code
        self.assertEqual(statuscode, 200)

        allentriesname()
        # Test status of all entries one by one
        for i in entries:
            response=tester.get("/contactbook/"+i)
            statuscode=response.status_code
            self.assertEqual(statuscode, 200)

    #test if content type is in json format 
    def test_content_type(self):
        
        #Test if all entries are in json format
        tester=app.test_client(self)
        response=tester.get("/contactbookentries")
        self.assertEqual(response.content_type, "application/json")

        #Test every entry one by one to determine all of them are in json format
        for i in entries:
            response=tester.get("/contactbook/"+i)
            self.assertEqual(response.content_type, "application/json")


    

if __name__== "__main__":
    unittest.main()


