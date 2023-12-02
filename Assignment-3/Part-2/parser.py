#-------------------------------------------------------------------------
# AUTHOR: Isaiah Hessler
# FILENAME: parser.py
# SPECIFICATION: By using the data persisted in the previous question, write a Python program parser.py that
# will read the CS faculty information, parse faculty members name, title, office, email, and website, and
# persist this data in MongoDB.
# FOR: CS 4250- Assignment #3
# TIME SPENT: 5 hours
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

    db2 = client['parser']
    collection2 = db2['professors']

    bs = BeautifulSoup(html_data, 'html.parser')

    divs = bs.find_all('div', class_="clearfix")

    #name, title, office, email, and website
    counter = 0
    for div in divs:
        #print(div.find_all("p"))
        #div_id = counter
        for x in div.find_all(string=re.compile(r"^[A-Z]")):
            flag = False
            y = x.find_next(text=lambda t: "" in t.text)
            for i in y:
                if (i.isalpha() or i.isnumeric()):
                    flag = True
            if flag == True:
                y = y.lstrip(": ")
            else:
                y = y.find_next(text=lambda t: "" in t.text)
            print(x)
            print(y)
            print("-----")
        #x = div(text=lambda t: "Title" in t.text)
        #print(div())
        #name = div.find('strong', string="").get_text(strip=True)
        #title =
        #office =
        #email =
        #website =

        counter += 1



parse_page()