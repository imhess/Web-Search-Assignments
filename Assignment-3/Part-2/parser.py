#-------------------------------------------------------------------------
# AUTHOR: Isaiah Hessler
# FILENAME: parser.py
# SPECIFICATION: By using the data persisted in the previous question, write a Python program parser.py that
# will read the CS faculty information, parse faculty members name, title, office, email, and website, and
# persist this data in MongoDB.
# FOR: CS 4250- Assignment #3
# TIME SPENT: 8 hours
#-----------------------------------------------------------*/
from pymongo import MongoClient
from bs4 import BeautifulSoup
import re

def parse_page():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['crawler']
    collection = db['pages']
    url = 'https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml'

    page = collection.find_one({'_id': url})
    html_data = page['html']

    client.close()

    bs = BeautifulSoup(html_data, 'html.parser')

    divs = bs.find_all('div', class_="clearfix")

    attributeList = []
    id_counter = 0
    for div in divs:
        counter = 0
        for x in div.find_all(string=re.compile(r"^[A-Z]")):
            flag = False
            y = x.find_next(string=lambda t: "" in t.text)
            for i in y:
                if (i.isalpha() or i.isnumeric()):
                    flag = True
            if flag == True:
                y = y.lstrip(": ")
            else:
                y = y.find_next(string=lambda t: "" in t.text)
            y = y.replace(u'\xa0', u'')
            y = y.rstrip(" ")
            if counter != 0:
                attributeList.append(y)
            else:
                attributeList.append(x)
            counter += 1
        if attributeList != []:
            print(attributeList)
            store({"_id": id_counter, "name": attributeList[0], "title": attributeList[1], "office": attributeList[2], "email": attributeList[4], "website": attributeList[5]})
            id_counter += 1
        attributeList.clear()

def store(data):
    client = MongoClient('mongodb://localhost:27017/')
    db2 = client['parser']
    collection2 = db2['professors']
    collection2.update_one({'_id': data['_id']}, {'$set': data}, upsert=True)
    client.close()

parse_page()
