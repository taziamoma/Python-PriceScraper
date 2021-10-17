import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

url = 'https://www.propertyroom.com/c/electronics/'

productList = dict()
nameList = []
priceList = []

def get_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def parse(soup):
    results = soup.find_all('div', {'class': 'col-products span_1_of_5 ListingContainer'})
    print(len(results))
    for item in results:
        price_count = 0
        price_tag = "time-bids-category"

        name = item.find('div', {'class': 'product-name-category'}).text.strip()
        price = item.find('div', {'class': price_tag}).text.strip().split('$')[1].lstrip()

        nameList.append(name)
        priceList.append(price)

        #print(product)
        price_count+= 1

    return

soup = get_data(url)
product = parse(soup)
print(nameList)
print(priceList)


