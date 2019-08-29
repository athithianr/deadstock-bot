from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import platform
options = Options()
options.headless = True
new_arrivals_page_url = 'https://www.deadstock.ca/collections/new-arrivals'
size = 9.5

if platform.system() == 'Darwin':
    driver = webdriver.Chrome(r'/Users/arajkumar/Desktop/deadstock-bot/chromedriver', options=options)
elif platform.system()== 'Windows':
    driver = webdriver.Chrome(r'C:\Users\athit\Desktop\deadstock-bot\windows_chromedriver.exe', options=options)

def add_shoe_to_cart(size):
    start_time = time.time() 
    driver.get(new_arrivals_page_url)
    e = driver.find_element_by_id('ProductSelect-option-US Size-{}'.format(size))
    driver.execute_script("arguments[0].click();", e)
    print("Found size {}...".format(size))
    b = driver.find_element_by_id('AddToCartForm1')
    driver.execute_script("arguments[0].submit();", b)
    print("Added shoes to cart...")
    print ("Added to cart in", time.time() - start_time)
    checkout_cart()

def checkout_cart():
        driver.get('https://www.deadstock.ca/cart')        
        class_element = driver.find_element_by_name('checkout')
        driver.execute_script("arguments[0].click();", class_element)
        print("Proceeding to checkout page...")


# def fetch_link_from_new_arrivals_page(new_arrivals_page_url):
#     driver.get(new_arrivals_page_url)
#     e = driver.find_element_by_class_name('grid-product__meta')
#     product_url = e.get_attribute('href')
#     print("Found product link: {}".format(product_url))
#     driver.get(product_url)
#     return product_url

# def add_shoe_to_cart(size):
#     product_url = fetch_link_from_new_arrivals_page(new_arrivals_page_url)
#     e = driver.find_element_by_id('ProductSelect-option-US Size-{}'.format(size))
#     driver.execute_script("arguments[0].click();", e)
#     print("Found size {}...".format(size))
#     b = driver.find_element_by_id('AddToCart')
#     driver.execute_script("arguments[0].click();", b)
#     print("Added shoes to cart...")

if __name__ == '__main__':
    add_shoe_to_cart(size)


