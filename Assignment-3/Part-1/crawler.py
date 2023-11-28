from urllib.request import urlopen
from urllib.parse import urljoin
from pymongo import MongoClient
from bs4 import BeautifulSoup

frontier = 'https://www.cpp.edu/sci/computer-science/'
target = "Permanent Faculty"
next_link = []
visit_later = []
crawled_urls = set()

def search_for_page(url, target):

    while url not in crawled_urls:
        html = urlopen(url)
        page = html.read()
        bs = BeautifulSoup(page, 'html.parser')
        html_data = page.decode('utf-8')

        if bs.find('h1', {'class':'cpp-h1'}, string=target):
            print(" ")
            print(f"Page found. {url}")
            return True

        crawled_urls.add(url)

        store({"_id": url, "html": html_data})

        next_link = bs.find_all('a')
        if next_link:
            for link in next_link:
                if link not in crawled_urls:
                    link = urljoin(url, link['href'])
                    visit_later.append(link)
                    print(link)
        else:
            break
    
    next_link.clear()
    return False

def store(data):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['crawler']
    collection = db['pages']
    collection.update_one({'_id': data['_id']}, {'$set': data}, upsert=True)
    client.close()

search_for_page(frontier, target)

for url in visit_later:
    if search_for_page(url, target) == True:
        break
    else:
        print(" ")
        print(f"Not found on page: {url}")
        print(" ")