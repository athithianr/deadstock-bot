import requests
import time
from bs4 import BeautifulSoup as bs
import re
import platform
from selenium import webdriver

new_arrivals_page_url = 'https://shop.havenshop.com/collections/new-arrivals'
base_url = 'https://havenshop.com'
post_url = 'https://shop.havenshop.com/cart/add.js'
keywords = ['daybreak', 'lavender']
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
        "a", {'class': re.compile('product-card nike'), 'href': re.compile("|".join(keywords))})
    if href_link is None:
        time.sleep(1)
    else:
        break

product_page_url = href_link.get('href')
print("Acquired product page url: {}".format(product_page_url))

r = requests.get(product_page_url).text
soup = bs(r, 'lxml')
product_variants = soup.find('select', {'id': 'product-select', 'name': 'id'})
for size_option in product_variants:
    try:
        if '{}US'.format(size) in size_option.text:
            id = size_option.get('value')
            break
    except AttributeError:
        pass

response = requests.post(post_url, data={'id': id, 'quantity': '1'})

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

print(response.cookies)

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
driver.get('https://shop.havenshop.com/cart')
