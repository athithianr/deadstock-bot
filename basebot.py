Class BaseBot(object):

    def __init__(self, sizes):
        self.shoe_sizes = []

    def check_platform_system(self):

        if platform.system() == 'Darwin':
            driver = webdriver.Chrome(r'C:\Users\athit\Desktop\deadstock-bot\mac_chromedriver')
        elif platform.system() == 'Windows':
            driver = webdriver.Chrome(r'C:\Users\athit\Desktop\deadstock-bot\windows_chromedriver.exe', options=options)
