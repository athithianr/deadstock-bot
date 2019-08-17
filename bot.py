from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import platform

options = Options()



new_arrivals_page_url = 'https://www.deadstock.ca/collections/new-arrivals'

if platform.system() == 'Darwin':
    driver = webdriver.Chrome(r'C:\Users\athit\Desktop\deadstock-bot\mac_chromedriver')
elif platform.system()== 'Windows':
    driver = webdriver.Chrome(r'C:\Users\athit\Desktop\deadstock-bot\windows_chromedriver.exe', options=options)

driver.get(new_arrivals_page_url)
size = 9.5


def fetch_link_from_new_arrivals_page(new_arrivals_page_url):
    e = driver.find_element_by_class_name('grid-product__meta')
    product_url = e.get_attribute('href')
    driver.get(product_url)
    return product_url

def add_shoe_to_cart(size):
    product_url = fetch_link_from_new_arrivals_page(new_arrivals_page_url)
    e = driver.find_element_by_id('ProductSelect-option-US Size-{}'.format(size))
    driver.execute_script("arguments[0].click();", e)
    b = driver.find_element_by_id('AddToCart')
    driver.execute_script("arguments[0].click();", b)


start_time = time.time()
add_shoe_to_cart(size)
print("--- %s seconds ---" % (time.time() - start_time))

