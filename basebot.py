from selenium import webdriver
import platform
from selenium.webdriver.chrome.options import Options


class BaseBot:

    def __init__(self):
        self.shoe_sizes = []
        self.base_url = ''
        self.options = Options()
        self.check_platform_system()
        self.payment_method = ''

    def check_platform_system(self):
        if platform.system() == 'Darwin':
            self.driver = webdriver.Chrome(r'/Users/arajkumar/Desktop/deadstock-bot/chromedriver', options=self.options)
        elif platform.system() == 'Windows':
            self.driver = webdriver.Chrome(r'C:\Users\athit\Desktop\deadstock-bot\windows_chromedriver.exe', options=self.options)

    