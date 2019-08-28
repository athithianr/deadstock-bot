import requests
import time
from bs4 import BeautifulSoup as bs
import re

size = 9
size_str = str(size)
new_arrivals_page_url = 'https://www.deadstock.ca/collections/new-arrivals'
url = 'https://www.deadstock.ca'
post_url = 'https://www.deadstock.ca/cart/add.js'

cart_time = time.time()
retries = 1
while retries <= 3:
    resp = requests.get(new_arrivals_page_url).text
    soup = bs(resp, 'lxml')
    print('Trying to find keyword, attempt {}...'.format(retries))
    link = soup.find("a", {'class': 'grid-product__meta', 'href': re.compile('raptors')})
    if link is None:
        time.sleep(retries)
        retries += 1
    else:
        break

product_page_url = url + link.get('href')
print("Acquired product url: {}".format(product_page_url))

r = requests.get(product_page_url).text
soup = bs(r, 'lxml')
# product_variants = soup.find('select', id='ProductSelect')
option = soup.find('option', {'data-sku': re.compile(size_str)})
id = option.get('value')
# for size_option in product_variants:
#     try:
#         if '{} -'.format(size) in size_option.text:
#             id = size_option.get('value')
#             break
#     except AttributeError:
#         pass

response = requests.request("POST", post_url, data={'id': id})

if id and response.status_code == 200:
    print("Added item to cart...")
else:
    print("Unable to add item to cart...")

print("Carted in", time.time() - cart_time)

cart_cookies = [
    {
        'name': 'cart',
        'value': ''
    },
    {
        'name': 'cart_ts',
        'value': ''
    },
    {
        'name': 'cart_sig',
        'value': ''
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
elif platform.system() == 'Windows':
    driver = webdriver.Chrome(r'C:\Users\athit\Desktop\deadstock-bot\windows_chromedriver.exe')

print("Navigating to dummy url to add cookies in browser...")
driver.get(url + dummy_url)

for cookie in cart_cookies:
    driver.add_cookie(cookie)
print("Navigating to cart...")
driver.get(url + '/cart')
