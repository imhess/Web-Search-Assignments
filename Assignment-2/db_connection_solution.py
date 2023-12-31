#-------------------------------------------------------------------------
# AUTHOR: Isaiah Hessler
# FILENAME: Assignment-2, db_connection.py
# SPECIFICATION: Complete the Python program (db_connection.py) that will use the corpus database tables
# created in question 1 to manage an inverted index.
# FOR: CS 4250- Assignment #1
# TIME SPENT: 12 Hours +
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
import psycopg2
from psycopg2.extras import RealDictCursor

def connectDataBase():

    # Create a database connection object using psycopg2
    DB_NAME = "corpus"
    DB_USER = "postgres"
    DB_PASS = "012202"
    DB_HOST = "localhost"
    DB_PORT = "5432"

    try:
        conn = psycopg2.connect(database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT,
        cursor_factory=RealDictCursor)
        return conn
    except:
        print("Database not connected successfully")

def createCategory(cur, catId, catName):

    # Insert a category in the database
    sql = "Insert into category (catId, catName) Values (%s, %s)"

    catSet = [catId, catName]
    cur.execute(sql, catSet)

def createDocument(cur, docId, docText, docTitle, docDate, docCat):
    # 1 Get the category id based on the informed category name
    sql = "Select catid from category where catname = %s"
    catname = [docCat]
    cur.execute(sql, catname)
    value = cur.fetchall()
    category_id = value[0]['catid']


    # 2 Insert the document in the database. For num_chars, discard the spaces and punctuation marks.
    stringcount = 0
    for i in docText:
        if i.isalpha() == True: 
            stringcount += 1
    sql = "Insert into documents (docid, doctext, doctitle, num_chars, docdate, doccat) Values (%s, %s, %s, %s, %s, %s)"

    docset = [docId, docText, docTitle, stringcount, docDate, category_id]
    cur.execute(sql, docset)

    # 3 Update the potential new terms.
    # 3.1 Find all terms that belong to the document. Use space " " as the delimiter character for terms and Remember to lowercase terms and remove punctuation marks.
    punctuation = {'.', ',', '!', '?', ':', ';', '[', ']', '(', ')', '{', '}', '/', '\\'}
    for j in range(len(docText)):
        for i in punctuation:
            x = docText.replace(i, '')
            docText = x
    docText = docText.lower()
    terms = []
    terms = docText.split(" ")
    terms = list(set(terms))
    terms.sort()

    # 3.2 For each term identified, check if the term already exists in the database
    # 3.3 In case the term does not exist, insert it into the database
    for term in terms:
        sql = "Select term from terms where term = %s"
        termname = [term]
        cur.execute(sql, termname)
        result = cur.fetchall()
        if not result:
            termlength = len(term)
            sql = "Insert into terms (term, num_chars) Values (%s, %s)"

            termset = [term, termlength]
            cur.execute(sql, termset)

    # 4 Update the index
    # 4.1 Find all terms that belong to the document
    list_of_terms = []
    for term in terms:
        sql = "Select term from terms where term = %s"
        termname = [term]
        cur.execute(sql, termname)
        result = cur.fetchall()
        list_of_terms.append(result[0]['term'])

    # 4.2 Create a data structure the stores how many times (count) each term appears in the document
    # 4.3 Insert the term and its corresponding count into the database
    terms2 = docText.split()
    for term in terms:
        docCount = terms2.count(term)
        sql = "Insert into term_count (countdoc, countterm, count) Values (%s, %s, %s)"

        countset = [docId, term, docCount]
        cur.execute(sql, countset)

def deleteDocument(cur, docId):

    # 1 Query the index based on the document to identify terms
    # 1.1 For each term identified, delete its occurrences in the index for that document
    # 1.2 Check if there are no more occurrences of the term in another document. If this happens, delete the term from the database.
    counter = 0
    sql = "Select countterm from term_count where countdoc = %s"
    document_id = [docId]
    cur.execute(sql, document_id)
    term_list = cur.fetchall()
    for term in term_list:
        current_term = term_list[counter]['countterm']
        sql = "Delete from term_count where countdoc = %s and countterm = %s"
        deleteset = [docId, current_term]
        cur.execute(sql, deleteset)

        sql = "Select * from term_count where countterm = %s"
        select_term = [current_term]
        cur.execute(sql, select_term)
        result = cur.fetchall()
        if not result:
            sql = "Delete from terms where term = %s"
            delete_term = [current_term]
            cur.execute(sql, delete_term)
        counter += 1

    # 2 Delete the document from the database
    sql = "Delete from documents where docid = %s"
    delete_doc = [docId]
    cur.execute(sql, delete_doc)

def updateDocument(cur, docId, docText, docTitle, docDate, docCat):

    #sql = "Update documents set docid = %s, doctext = %s, doctitle = %s, numchars = %s, docdate = %s, doccat = %s"

    # 1 Delete the document
    deleteDocument(cur, docId)

    # 2 Create the document with the same id
    createDocument(cur, docId, docText, docTitle, docDate, docCat)

def getIndex(cur):

    # Query the database to return the documents where each term occurs with their corresponding count.
    counter_terms = 0
    counter_docs = 0
    sql = "Select term from terms"
    cur.execute(sql)
    results = cur.fetchall()
    for term in results:
        current_term = results[counter_terms]['term']
        sql = "Select * from term_count where countterm = %s"
        find_term = [current_term]
        cur.execute(sql, find_term)
        count_list = cur.fetchall()
        print(f'{current_term}:')
        for row in count_list:
            current_document = count_list[counter_docs]['countdoc']
            current_count = count_list[counter_docs]['count']
            sql = "Select doctitle from documents where docid = %s"
            find_document = [current_document]
            cur.execute(sql, find_document)
            doc_list = cur.fetchall()
            current_doc_title = doc_list[0]['doctitle']
            print(f'{current_doc_title}: {current_count}')
            counter_docs += 1
        print(' ')
        counter_terms += 1
        counter_docs = 0
