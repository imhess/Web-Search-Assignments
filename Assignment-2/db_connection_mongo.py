#-------------------------------------------------------------------------
# AUTHOR: Isaiah Hessler
# FILENAME: db_connection_mongo.py
# SPECIFICATION: complete the Python program (db_connection_mongo.py) by using
# PyMongo. Requirements: 1) use the driver program index_mongo.py to trigger the operations
# FOR: CS 4250- Assignment #2
# TIME SPENT: 5 hours
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
from pymongo import MongoClient

def connectDataBase():

    # Create a database connection object using pymongo
    client = MongoClient("mongodb://localhost:27017/")
    db = client["corpus"]
    collection = db["documents"]


#def createDocument(col, docId, docText, docTitle, docDate, docCat):

    # create a dictionary to count how many times each term appears in the document.
    # Use space " " as the delimiter character for terms and remember to lowercase them.
    # --> add your Python code here

    # create a list of dictionaries to include term objects.
    # --> add your Python code here

    #Producing a final document as a dictionary including all the required document fields
    # --> add your Python code here

    # Insert the document
    # --> add your Python code here

#def deleteDocument(col, docId):

    # Delete the document from the database
    # --> add your Python code here

#def updateDocument(col, docId, docText, docTitle, docDate, docCat):

    # Delete the document
    # --> add your Python code here

    # Create the document with the same id
    # --> add your Python code here

#def getIndex(col):

    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    # ...
    # --> add your Python code here