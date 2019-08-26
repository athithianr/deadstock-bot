import requests
import time
import platform
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import lxml

if platform.system() == 'Darwin':
    driver = webdriver.Chrome(r'/Users/arajkumar/Desktop/deadstock-bot/chromedriver')
elif platform.system()== 'Windows':
    driver = webdriver.Chrome(r'C:\Users\athit\Desktop\deadstock-bot\windows_chromedriver.exe')

start_time = time.time() 
base_url = 'https://www.deadstock.ca/collections/new-arrivals/products/puma-rs-x-core-puma-white'
post_url = 'https://www.deadstock.ca/cart/add.js'
url = 'https://www.deadstock.ca'
size = 9
cart_time = time.time()
r = requests.get(base_url).text
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

headers = {
    'id': id,
}

response = requests.request("POST", post_url, data=headers)

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

driver.get(url)

for cookie in cart_cookies:
    driver.add_cookie(cookie)

print ("My program took", time.time() - start_time, "to run")
