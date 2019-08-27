import requests
import time
from bs4 import BeautifulSoup as bs
import lxml
import re

size = 8
new_arrivals_page_url = 'https://www.deadstock.ca/collections/new-arrivals'
url = 'https://www.deadstock.ca'
post_url = 'https://www.deadstock.ca/cart/add.js'

cart_time = time.time()
retries = 1
while retries <=4:
    resp = requests.get(new_arrivals_page_url).text
    soup = bs(resp, 'lxml')
    print('Trying to find keyword, attempt {}...'.format(retries))
    link = soup.find("a",{'class':'grid-product__meta', 'href': re.compile('university')})
    if link == None:
        time.sleep(retries)
        retries +=1
    else:
        break

product_page_url = url + link.get('href')
print("Acquired product url: {}".format(product_page_url))

r = requests.get(product_page_url).text
soup = bs(r, 'lxml')
product_variants = soup.find('select', id='ProductSelect')

for size_option in product_variants:
    try:
        if '{} -'.format(size) in size_option.text:
            id = size_option.get('value')
            print('Size {} is in stock...'.format(size))
            break
    except AttributeError:
        pass        

response = requests.request("POST", post_url, data={'id':id})

if response.status_code == 200:
    print("Added item to cart...")

print ("Carted in", time.time() - cart_time)

cart_cookies = [
    {
        'name':'cart',
        'value':''
    },
    {
        'name':'cart_ts',
        'value':''
    },
    {
        'name':'cart_sig',
        'value':''
    }
]

for cookie in response.cookies:
    if cookie.name == 'cart':
        cart_cookies[0]['value'] = cookie.value
    elif cookie.name == 'cart_ts':
        cart_cookies[1]['value'] = cookie.value
    elif cookie.name == 'cart_sig':
        cart_cookies[2]['value'] = cookie.value

dummy_url = '/404error'

from selenium import webdriver
import platform

if platform.system() == 'Darwin':
    driver = webdriver.Chrome(r'/Users/arajkumar/Desktop/deadstock-bot/chromedriver')
elif platform.system()== 'Windows':
    driver = webdriver.Chrome(r'C:\Users\athit\Desktop\deadstock-bot\windows_chromedriver.exe')

print("Navigating to dummy url to add cookies in browser...")
driver.get(url + dummy_url)

for cookie in cart_cookies:
    driver.add_cookie(cookie)

driver.get(url)