import platform
from selenium import webdriver
import requests
import time
from bs4 import BeautifulSoup as bs
import re

new_arrivals_page_url = 'https://nrml.ca/collections/new-arrivals'
base_url = 'https://nrml.ca/'
post_url = 'https://nrml.ca/cart/add.js'
keywords = ['raptors', 'shox']
size = 12
size_str = str(size)

s = requests.Session()
s.headers.update(
    headers={
        'User-Agent': '"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0"',
    }
)
cart_time = time.time()
for retries in range(5):
    resp = requests.get(new_arrivals_page_url).text
    soup = bs(resp, 'lxml')
    print('Trying to find keywords, attempt {}...'.format(retries+1))
    href_link = soup.find(
        "a", {'class': 'grid__image', 'href': re.compile("|".join(keywords))})
    if href_link is None:
        time.sleep(1)
    else:
        break

product_page_url = base_url + href_link.get('href')
print("Acquired product page url: {}".format(product_page_url))

r = requests.get(product_page_url).text
soup = bs(r, 'lxml')
option = soup.find('div', {'class': 'option__variant',
                           'data-variant-title': size_str})
if int(option.get('data-stock')) > 0:
    id = option.get('data-variant-id')
else:
    print("Sold out...")
response = requests.post(
    post_url, data={'id': id, 'form_type': 'product', 'utf8': '✓', 'quantity': '1'})

if id and response.status_code == 200:
    print("Added item to cart...")
    print("Carted in", time.time() - cart_time)
else:
    print("Unable to add item to cart...")

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


if platform.system() == 'Darwin':
    driver = webdriver.Chrome(
        r'/Users/arajkumar/Desktop/deadstock-bot/chromedriver')
elif platform.system() == 'Windows':
    driver = webdriver.Chrome(
        r'C:\Users\athit\Desktop\deadstock-bot\windows_chromedriver.exe')

print("Navigating to dummy url to add cookies in browser...")
driver.get(base_url + dummy_url)

for cookie in cart_cookies:
    driver.add_cookie(cookie)
print("Navigating to cart...")
driver.get(base_url + '/cart')
