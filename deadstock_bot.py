import time
from basebot import BaseBot


class DeadstockBot(BaseBot):

    def __init__(self):
        super().__init__()
        self.shoe_sizes = [9]
        self.base_url = 'https://www.deadstock.ca/collections/new-arrivals'
        self.payment_method = 'Paypal'
    
    #def check_for_shoes(self):

  
    def add_shoe_to_cart(self):
        self.driver.get(self.base_url)
        for size in self.shoe_sizes:
            e = self.driver.find_element_by_id('ProductSelect-option-US Size-{}'.format(size))
        print("----Size found----")
        self.driver.execute_script("arguments[0].click();", e)
        b = self.driver.find_element_by_id('AddToCartForm1')
        self.driver.execute_script("arguments[0].submit();", b)
        print("----Adding to Cart----")
        self.checkout_cart()
    
    def checkout_cart(self):
        self.driver.get('https://www.deadstock.ca/cart')        
        class_element = self.driver.find_element_by_name('checkout')
        self.driver.execute_script("arguments[0].click();", class_element)
        print("----Checking out cart----")
        
        # if(self.payment_method == 'Paypal'):
        #     express_checkout_paypal()
    
#def express_checkout_paypal(self):
        

        
if __name__ == '__main__':
    start_time = time.time()
    obj = DeadstockBot()
    obj.add_shoe_to_cart()
    print("--- %s seconds ---" % (time.time() - start_time))
