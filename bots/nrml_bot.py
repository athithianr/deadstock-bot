import requests
import time
from bs4 import BeautifulSoup as bs
import re
import webbrowser
from threading import Thread


new_arrivals_page_url = 'https://nrml.ca/collections/nrml-footwear'
base_url = 'https://nrml.ca'
keywords = ['icon', 'sail']
sizes = ['9.5', '7']


# Check new arrivals page for specified keywords
def get_product_page_url():
    threads = []
    links = []
    for retries in range(15):
        response = session.get(new_arrivals_page_url).text
        soup = bs(response, 'lxml')
        print('Trying to find keywords, attempt {}...'.format(retries+1))
        grid_image_objects = soup.findAll(
            "a", {'href': re.compile("|".join(keywords), re.IGNORECASE), 'class': 'grid__image'})
        if not grid_image_objects:
            time.sleep(0.420)
        else:
            for obj in grid_image_objects:
                if obj.get('href') not in links:
                    links.append(obj.get('href'))
            break
    for link in links:
        product_page_url = base_url + link
        print("Acquired product page url: {}".format(product_page_url))
        process = Thread(target=add_to_cart, args=[product_page_url])
        process.start()
        threads.append(process)
    for process in threads:
        process.join()


# Find variant id of shoe and open checkout page
def add_to_cart(product_page_url):
    checkout_url = base_url +'/cart/'
    url_changed = False
    print('Trying to find sizes for {}'.format(product_page_url))
    r = session.get(product_page_url).text
    soup = bs(r, 'lxml')
    for size in sizes:
        option = soup.find('div', {'class': 'option__variant',
                                   'data-variant-title': size})
        if option:
            if int(option.get('data-stock')) > 0:
                id = option.get('data-variant-id')
                print("Size {} is Available...".format(size))
                checkout_url += '{}:1,'.format(id)
                url_changed = True
            else:
                print("Size {} sold out...".format(size))
    if url_changed:
        webbrowser.open(checkout_url)


if __name__ == "__main__":
    total_time = time.time()
    session = requests.Session()
    session.headers.update(
        {'User-Agent': '"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0"'}
    )
    get_product_page_url()
    print("Total time: ", time.time() - total_time)
