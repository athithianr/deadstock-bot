import requests
import time
from bs4 import BeautifulSoup as bs
import re
import webbrowser


sizes = ['7', '9.5']
new_arrivals_page_url = 'https://www.capsuletoronto.com/collections/new-arrivals'
base_url = 'https://www.capsuletoronto.com'
keywords = ['viotech', '90']


def get_product_page_url():
    for retries in range(15):
        resp = session.get(new_arrivals_page_url).text
        soup = bs(resp, 'lxml')
        print('Trying to find keywords, attempt {}...'.format(retries+1))
        href_link = soup.find(
            "a", {'class': 'product-card', 'href': re.compile("|".join(keywords), re.IGNORECASE)})
        if href_link is None:
            time.sleep(1)
        else:
            break
    product_page_url = base_url + href_link.get('href')
    print("Acquired product page url: {}".format(product_page_url))
    checkout_page(product_page_url)


def checkout_page(product_page_url):
    response = session.get(product_page_url).text
    soup = bs(response, 'lxml')
    size_collected = 0
    options = soup.findAll(
        "option")
    for option in options:
        if option.get('value') in sizes:
            continue

        if size_collected == len(sizes):
            break
        else:
            if option.text.strip() in sizes:
                id = option.get('value')
                webbrowser.open_new(
                    base_url + '/cart/{}:1'.format(id))
                print("Navigating to checkout size {}".format(option.text.strip()))
                size_collected += 1

if __name__ == "__main__":
    total_time = time.time()
    session = requests.Session()
    session.headers.update(
        {'User-Agent': '"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0"'}
    )
    get_product_page_url()
    print("Total time: ", time.time() - total_time)
