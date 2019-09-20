import requests
import time
from bs4 import BeautifulSoup as bs
import re
import webbrowser


sizes = [12, 13]
size = 8
new_arrivals_page_url = 'https://offthehook.ca/collections/new-arrivals'
base_url = 'https://offthehook.ca'
keywords = ['gel', 'fujitrabuco']


def get_variant_id():
    for retries in range(15):
        response = session.get(new_arrivals_page_url).text
        soup = bs(response, 'lxml')
        print('Trying to find keywords, attempt {}...'.format(retries+1))
        href_link = soup.find(
            "a", {'data-value': str(size), 'href': re.compile("|".join(keywords))})
        if href_link is None:
            time.sleep(1)
        else:
            break
    id = href_link.get('href').split("variant=")[1]
    webbrowser.open_new(base_url + '/cart/{}:1'.format(id))


if __name__ == "__main__":
    total_time = time.time()
    session = requests.Session()
    session.headers.update(
        {'User-Agent': '"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0"'}
    )
    get_variant_id()
    print("Total time: ", time.time() - total_time)
