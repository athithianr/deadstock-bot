from selenium import webdriver
import requests
import time
from bs4 import BeautifulSoup as bs
import re
from notify_run import Notify
from threading import Thread


sizes = ['8', '8.5', '9', '9.5']
new_arrivals_page_url = 'https://www.ssense.com/en-us/women/designers/nike'
base_url = 'https://www.ssense.com'
post_url = 'https://www.ssense.com/en-ca/api/shopping-bag/'
keywords = ['vapormax']
cart_time = time.time()


def get_product_page_url():
    fem_retries = 0
    threads = []
    while True:
        resp = session.get(new_arrivals_page_url).text
        soup = bs(resp, 'lxml')
        print('Trying to find keywords, attempt {} on Female site...'.format(fem_retries+1))
        href_links = soup.findAll(
            "a", {'href': re.compile("|".join(keywords), re.IGNORECASE)})
        if href_links is None:
            fem_retries += 1
            time.sleep(5)
        else:
            break
    for link in href_links:
        product_page_url = base_url + link.get('href')
        print("Acquired product page url: {}".format(product_page_url))
        process = Thread(target=add_to_cart, args=[product_page_url])
        process.start()
        threads.append(process)

    for process in threads:
        process.join()


def add_to_cart(product_page_url):
    print('Trying to find sizes for {}'.format(product_page_url))
    r = session.get(product_page_url).text
    soup = bs(r, 'lxml')
    for size in sizes:
        option = soup.find('option', {'value': re.compile(size + '_')})
        try:
            id = option.get('value').split(size + '_')[1]
            session.post(
                post_url + id, data={'serviceType': 'product-details', 'sku': id})
            if id:
                print("Found size {} id...".format(size))
                print("Carted in", time.time() - cart_time)
        except AttributeError:
            print("Size {} sold out!".format(size))
            pass


if __name__ == "__main__":
    notify = Notify()
    notify.send('Script Started!')
    session = requests.Session()
    session.headers.update(
        {'User-Agent': '"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0"'}
    )
    get_product_page_url()
    driver = webdriver.Chrome(
        r'C:\Users\athit\Desktop\deadstock-bot\windows_chromedriver.exe')
    print("Navigating to dummy url to add cookies in browser...")
    dummy_url = '/404error'
    driver.get(base_url + dummy_url)
    for cookie in session.cookies:
        driver.add_cookie({'name': cookie.name, 'value': cookie.value})
    print("Navigating to cart...")
    driver.get(base_url + '/shopping-bag')
    notify.send('Script finished!')
