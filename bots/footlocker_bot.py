import platform
from selenium import webdriver
import requests
import time
from bs4 import BeautifulSoup as bs
import re
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PROXY = "64.235.204.107:8080"

size = 9.5
size_str = str(size)
keywords = ['airmax', '200']
cart_time = time.time()
early_link = 'https://www.footlocker.ca/en/product/nike-air-force-1-low-mens/04103873.html'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
link = 'https://www.footlocker.com/product/Jordan-Retro-13---Men-s/14571105.html'

def add_to_cart(link):
    driver.get(link)
    # element = driver.find_element_by_xpath('//*[@id="buyTools"]/div[1]/div[2]/label[8]')
    # element.click()
    # element1 = driver.find_element_by_css_selector('.ncss-btn-primary-dark.btn-lg.css-y0myut.addToCartBtn')
    # element1.click()
    element = driver.find_element_by_xpath('//*[@id="ProductDetails"]/div[5]/div[2]/fieldset/div/div[6]/label/span')
    element.click()
    element1 = driver.find_element_by_css_selector('.Button.ProductDetails-form__action')
    element1.click()
if __name__ == "__main__":
    # specify the desired user agent
    options = Options()
    options.add_argument('user-agent={}'.format(user_agent))
    options.add_argument('start-maximized')
    options.add_argument('--proxy-server={}'.format(PROXY))
    options.add_argument("no-sandbox")
    if platform.system() == 'Darwin':
        driver = webdriver.Chrome(
            r'/Users/arajkumar/Desktop/deadstock-bot/chromedriver')
    elif platform.system() == 'Windows':
        driver = webdriver.Chrome(
            r'C:\Users\athit\Desktop\deadstock-bot\test\windows_chromedriver.exe', options=options)
    driver.delete_all_cookies()
    add_to_cart(link)
