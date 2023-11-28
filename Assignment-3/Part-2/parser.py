from pymongo import MongoClient
from bs4 import BeautifulSoup

def open_page():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['crawler']
    collection = db['pages']
    html = 