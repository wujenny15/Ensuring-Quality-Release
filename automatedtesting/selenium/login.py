from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from chromedriver_py import binary_path # this will get you the path variable
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.common.by import By
import unittest

class SwayLabs(unittest.TestCase):
    @classmethod
    def setUp(inst):
        print ('Starting the browser...')
        # --uncomment when running in Azure DevOps.
        options = ChromeOptions()
        options.add_argument("--headless") 
        options.add_argument('--no-sandbox')

        inst.driver = webdriver.Chrome(options=options,executable_path=binary_path)
        # inst.driver = webdriver.Chrome(options=options)

        # inst.driver = webdriver.Chrome(executable_path=binary_path)
        print ('Browser started successfully. Navigating to the demo page to login.')
        inst.driver.get('https://www.saucedemo.com/')
        inst.wait = WebDriverWait(inst.driver, 5)

    def login(self, user, password):
        usernameTxt = self.wait.until(presence_of_element_located((By.ID, 'user-name')))
        passwordTxt = self.wait.until(presence_of_element_located((By.ID, 'password')))
        loginBtn = self.wait.until(presence_of_element_located((By.ID, 'login-button')))
        print ('Login with username: {0}'.format(user))
        usernameTxt.send_keys(user)
        print ('Login with password: {0}'.format(password))
        passwordTxt.send_keys(password)
        print('Click Login button')
        loginBtn.click()
        print('User {0} logs in successfully'.format(user))

    def add_or_remove_all_products(self,action):
            productsContainer = self.driver.find_element(By.ID,'inventory_container')
            products = productsContainer.find_elements_by_css_selector('.inventory_item')
            for idx, product in enumerate(products):
                productName = product.find_element_by_css_selector('.inventory_item_label a').text
                cartBtn = product.find_element_by_css_selector('.btn_inventory')
                cartBtn.click()
                print('{0} {1} products, product is: {2}'.format(action,idx+1,productName))  

    def test_log_in(self): 
        # Start the browser and login with standard_user
        self.login('standard_user', 'secret_sauce')

    def test_add_and_remove_all_products(self): 
        self.login('standard_user', 'secret_sauce')
        
        action = "Add"
        self.add_or_remove_all_products(action)
        cartBadge = self.driver.find_element_by_css_selector('#shopping_cart_container span').text
        assert cartBadge == '6' , 'Cart Badge has 6 products'
        print('All products are added to the shopping cart')

        action ="Remove"
        self.add_or_remove_all_products(action)
        cartBadge =self.driver.find_element_by_css_selector('#shopping_cart_container').text
        assert cartBadge == '' , 'Cart Badge has 0 products'
        print('All products are removed from the shopping cart')

    @classmethod
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()