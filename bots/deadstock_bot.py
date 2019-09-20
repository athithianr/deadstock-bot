import requests
import time
from bs4 import BeautifulSoup as bs
import re
import webbrowser
import threading


# sizes = ['9.5']
size = 9.5
new_arrivals_page_url = 'https://www.deadstock.ca/collections/new-arrivals'
base_url = 'https://www.deadstock.ca'
keywords = ['oil']
search_for_product_page = False


# def get_checkout_url_for_multiple_sizes():
#     size_collected = 0
#     for retries in range(15):
#         response = session.get(new_arrivals_page_url).text
#         soup = bs(response, 'lxml')
#         print('Trying to find keywords, attempt {}...'.format(retries+1))
#         options = soup.findAll(
#             "option", {'data-sku': re.compile('|'.join(keywords), re.IGNORECASE)})
#         if not options:
#             time.sleep(0.4)
#         else:
#             break

#     for option in options:
#         if size_collected == len(sizes):
#             break
#         if option.text.strip() in sizes:
#             id = option.get('value')
#             webbrowser.open_new(base_url + '/cart/{}:1'.format(id))
#             print("Navigating to checkout size {}".format(option.text.strip()))
#             size_collected += 1


# def get_checkout_url_for_single_size():
#     for retries in range(15):
#         response = session.get(new_arrivals_page_url).text
#         soup = bs(response, 'lxml')
#         print('Trying to find keywords, attempt {}...'.format(retries+1))
#         regex_str = '(?=.+-{})'.format(size) + '(' + '|'.join(keywords) + ')'
#         option = soup.find(
#              "option", {'data-sku': re.compile(regex_str, re.IGNORECASE)})
#         if not option:
#             time.sleep(0.420)
#         else:
#             id = option.get('value')
#             webbrowser.open_new(base_url + '/cart/{}:1'.format(id))
#             print("Navigating to checkout size {}".format(option.text.strip()))
#             break


def get_checkout_url_for_single_size():
    for retries in range(15):
        response = session.get(new_arrivals_page_url).text
        soup = bs(response, 'lxml')
        print('Trying to find keywords, attempt {}...'.format(retries+1))
        for size in sizes:
            regex_str = '(?=.+-{})'.format(size) + '(' + '|'.join(keywords) + ')'
            option = soup.find(
                 "option", {'data-sku': re.compile(regex_str, re.IGNORECASE)})
            if not option:
                time.sleep(0.420)
            else:
                id = option.get('value')
         


if __name__ == "__main__":
    total_time = time.time()
    session = requests.Session()
    session.headers.update({'User-Agent': '"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0"'})
    get_checkout_url_for_single_size()
    print("Total time: ", time.time() - total_time)
