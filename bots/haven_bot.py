import requests
import time
from bs4 import BeautifulSoup as bs
import re
import webbrowser

new_arrivals_page_url = 'https://shop.havenshop.com/collections/new-arrivals'
base_url = 'https://shop.havenshop.com'
post_url = 'https://shop.havenshop.com/cart/add.js'
keywords = ['1970s']
sizes = ['9.5']


# Check new arrivals page for specified keywords
def get_product_page_url():
    for retries in range(15):
        resp = session.get(new_arrivals_page_url).text
        soup = bs(resp, 'lxml')
        print('Trying to find keywords, attempt {}...'.format(retries+1))
        href_link = soup.find(
            "a", {'href': re.compile("|".join(keywords), re.IGNORECASE)})
        if href_link is None:
            time.sleep(1)
        else:
            break
    product_page_url = href_link.get('href')
    print("Acquired product page url: {}".format(product_page_url))
    checkout_page(product_page_url)


# Find variant id of shoe and open checkout page
def checkout_page(product_page_url):
    checkout_url = base_url + '/cart/'
    response = session.get(product_page_url).text
    soup = bs(response, 'lxml')
    size_collected = 0
    options = soup.findAll(
        "option")
    for option in options:
        if size_collected == len(sizes):
            break
        else:
            for size in sizes:
                if '{}US'.format(size) in option.text.strip():
                    id = option.get('value')
                    print("Size {} is Available...".format(size))
                    checkout_url += '{}:1,'.format(id)
                    size_collected += 1
    webbrowser.open_new(checkout_url)
    print("Navigating to checkout size {}".format(size))


if __name__ == "__main__":
    total_time = time.time()
    session = requests.Session()
    session.headers.update(
        {'User-Agent': '"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0"'}
    )
    get_product_page_url()
    print("Total time: ", time.time() - total_time)
