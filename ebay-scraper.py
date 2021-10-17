import random
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
]

for i in range(1, 4):
    user_agent = random.choice(user_agent_list)

headers = {'User-Agent': user_agent}

PATH = "C:\Program Files (x86)\chromedriver.exe"
option = webdriver.ChromeOptions()
option.add_experimental_option("excludeSwitches", ["enable-automation"])
option.add_experimental_option('useAutomationExtension', False)
option.add_argument('--disable-blink-features=AutomationControlled')
option.add_argument("window-size=1280,800")
option.add_argument(f"user-agent={user_agent}")

driver = webdriver.Chrome(PATH, options = option)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")


def parse(soup):
    productlist = []
    results = soup.find_all('div', {'class': 's-item__info clearfix'})
    for item in results:
        product = {
            'title': item.find('h3', {'class': 's-item__title s-item__title--has-tags'}).text,
            'soldprice': float(item.find('span', {'class': 'POSITIVE'}).text.replace('$', '').replace(',', '').strip()),
            'solddate': item.find('span', {'class': 's-item__title--tagblock__COMPLETED'}).find('span', {
                'class': 'POSITIVE'}).text,
            'bids': item.find('span', {'class': 's-item__bids'}).text,
            'link': item.find('a', {'class': 's-item__link'})['href']
        }
        print(product)
        productlist.append(product)
    return productlist

def getPrice(item):
    result = item.find_element_by_class_name('s-item__detail.s-item__detail--primary').text.replace('$', '').replace(',', '').strip()

    if item:
        ans = result
    else:
        ans = "None"
    return ans

def getTitle(item):
    result = item.find_element_by_class_name('s-item__title').text

    if result:
        return result
    else:
        return "None"

def getLink(item):
    result = item.find_element_by_class_name('s-item__link').get_attribute('href')

    if result:
        return result
    else:
        return "None"

def getData(searchTerm):
    url = f'https://www.ebay.com/sch/i.html?_from=R40&_nkw={searchTerm}&_sacat=0&LH_TitleDesc=0&LH_PrefLoc=1&rt=nc&LH_Sold=1&LH_Complete=1'
    #url = "https://www.ebay.com"

    driver.get(url)
    wait = WebDriverWait(driver, 10)

    if driver.page_source.__contains__("Please verify yourself to continue"):
        input("Pausing for captcha")

    productlist = []

    results = driver.find_elements_by_class_name('s-item__info.clearfix')

    for item in results:
        product = {
            'title': getTitle(item),
            'price': getPrice(item),
            'link': getLink(item)
        }
        print(product)
        productlist.append(product)

    return productlist

def process(searchTerm):
    product_list = getData(searchTerm)
    """
    for item in product_list:
    if item['title'] == "None":
        product_list.remove(item)

    print(product_list)
    """


searchTerm =['New YVES SAINT LAURENT Sunglasses', 'GE Lighting C by GE Sol WiFi Connected Smart Light Fixture', 'Wireless Auto Remote Duplicator']


for item in searchTerm:
    process(item)