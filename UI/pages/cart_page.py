from time import sleep

from .base_page import BasePage
from .locators import CartPageLocators


class CartPage(BasePage):
    def click_continue_shopping_button(self):
        button = self.browser.find_element(*CartPageLocators.CONTINUE_SHOPPING_BUTTON)
        button.click()

    def click_minus_button(self):
        button = self.browser.find_element(*CartPageLocators.MINUS_BUTTON)
        button.click()

    def click_minus_2_button(self):
        button = self.browser.find_element(*CartPageLocators.MINUS_2_BUTTON)
        button.click()

    def click_plus_button(self):
        button = self.browser.find_element(*CartPageLocators.PLUS_BUTTON)
        button.click()

    def click_plus_2_button(self):
        button = self.browser.find_element(*CartPageLocators.PLUS_2_BUTTON)
        button.click()

    def get_product_cost(self):
        return self.browser.find_element(*CartPageLocators.PRODUCT_COST).text
    
    def get_product_2_cost(self):
        return self.browser.find_element(*CartPageLocators.PRODUCT_2_COST).text

    def get_subtotal(self):
        return self.browser.find_element(*CartPageLocators.SUBTOTAL).text        

    def is_cart_empty(self):
        self.is_element_present(*CartPageLocators.EMPTY_CART_MESSAGE)
    
    # check that amount changed after click "Plus" or "Minus"
    def is_change_amount(self, amount):
        amount_element = self.browser.find_element(*CartPageLocators.AMOUNT)
        if amount_element.text == amount:
            return True
        else: 
            return False   
    
    # check that product name on main page equal product name on cart page
    def is_product_in_cart(self, product_name):
        cart_page_product_name = self.browser.find_element(*CartPageLocators.PRODUCT_NAME)
        if cart_page_product_name.text == product_name:
            return True
        else:
            return False

    def remove_products(self):
        buttons = self.browser.find_elements(*CartPageLocators.REMOVE_BUTTON)                
        while len(buttons) > 0:            
            buttons[0].click()
            sleep(2)  # waiting is mandatory (do not remove)
            buttons = self.browser.find_elements(*CartPageLocators.REMOVE_BUTTON)            
