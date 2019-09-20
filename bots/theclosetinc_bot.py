import requests
import time
from bs4 import BeautifulSoup as bs
import re
import webbrowser

sizes = [7, 9.5, 11]
new_arrivals_page_url = 'https://www.theclosetinc.com/collections/new-arrivals'
base_url = 'https://www.theclosetinc.com'
post_url = 'https://www.theclosetinc.com/cart/add.js'
keywords = ['yeezy', 'inertia']


def get_product_page_url():
    for retries in range(15):
        response = session.get(new_arrivals_page_url).text
        soup = bs(response, 'lxml')
        print('Trying to find keywords, attempt {}...'.format(retries+1))
        href_link = soup.find(
            "a", {'itemprop': 'url', 'href': re.compile("|".join(keywords))})
        if href_link is None:
            time.sleep(1)
        else:
            break
    product_page_url = base_url + href_link.get('href')
    print("Acquired product page url: {}".format(product_page_url))
    add_to_cart(product_page_url)


def add_to_cart(product_page_url):
    response = session.get(product_page_url).text
    soup = bs(response, 'lxml')
    for size in sizes:
        option = soup.find('option', {'data-sku': re.compile('-' + str(size))})
        if option:
            if float(option.text) == size:
                id = option.get('value')
                webbrowser.open_new(base_url + '/cart/{}:1'.format(id))
        else:
            print("Size {} sold out...".format(size))



if __name__ == "__main__":
    total_time = time.time()
    session = requests.Session()
    session.headers.update(
        {'User-Agent': '"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0"'}
    )
    get_product_page_url()
    print("Total time: ", time.time() - total_time)
