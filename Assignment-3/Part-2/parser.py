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
        for strong_tag in div.find_all('strong'):
            text_data = strong_tag.nextSibling.next_sibling.strip()
            print(f"Data between </strong> and <br/>: {text_data}")
        #div_id = counter
        #name = div.find('strong', string="").get_text(strip=True)
        #title =
        #office =
        #email =
        #website =

        #counter += 1



parse_page()