import re
from typing import Literal

from selenium.common.exceptions import NoSuchElementException, \
                                       ElementClickInterceptedException, \
                                       ElementNotInteractableException

from .locators import BasePageLocators, HeaderLocators


class BasePage:

    def __init__(self, browser, url, timeout=4):
        self.browser = browser
        self.url = url
        self.browser.implicitly_wait(timeout)  # turn on implicitly wait  
        self.browser.maximize_window()
    
    def add_product_to_cart(self):
        button = self.browser.find_element(*BasePageLocators.ADD_TO_CART_BUTTON)
        button.click()
    
    def add_product_2_to_cart(self):
        button = self.browser.find_element(*BasePageLocators.ADD_TO_CART_BUTTON_2)
        button.click()

    def get_product_name(self):
        return self.browser.find_element(*BasePageLocators.PRODUCT_NAME).text
    
    def get_product_price(self):
        product_price_element = self.browser.find_element(*BasePageLocators.PRODUCT_PRICE).text
        return float(product_price_element[1:])
    
    def get_product_rating(self):
        product_rating = self.browser.find_element(*BasePageLocators.PRODUCT_RATING).text
        return product_rating
    
    def get_product_reviews(self):
        product_reviews_element = self.browser.find_element(*BasePageLocators.PRODUCT_REVIEWS).text
        pattern = re.compile(r'\b\d+\b')
        product_reviews = pattern.findall(product_reviews_element)
        return product_reviews[0]

    def get_product_weight(self):
        product_weight_element = self.browser.find_element(*BasePageLocators.PRODUCT_WEIGHT).text
        pattern = re.compile(r'\b\d+\b')
        product_weight = pattern.findall(product_weight_element)
        return product_weight[0]

    def go_to_cart_page(self):
        link = self.browser.find_element(*HeaderLocators.CART_LINK)
        link.click()
    
    def go_to_favorites_page(self):
        link = self.browser.find_element(*HeaderLocators.FAVORITES_PAGE_LINK)
        link.click()

    def go_to_login_page(self):
        link = self.browser.find_element(*HeaderLocators.LOGIN_LINK)
        link.click()

    def go_to_main_page(self):        
        main_page_link = self.browser.find_element(*HeaderLocators.MAIN_PAGE_LINK)
        main_page_link.click()

    def go_to_product_page(self):
        link = self.browser.find_element(*BasePageLocators.PRODUCT_LINK)
        link.click()

    def go_to_profile_page(self):        
        link = self.browser.find_element(*HeaderLocators.PROFILE_LINK)
        link.click()
    
    # check that amount on cart icon changed after adding product to cart 
    # and click "Plus" or "Minus"
    def is_change_cart_counter(self, amount):
        cart_counter = self.browser.find_element(*HeaderLocators.CART_COUNTER)
        if cart_counter.text == amount:
            return True
        else: 
            return False

    # check that amount on favorites page icon changed
    def is_change_favorites_counter(self, amount):
        favorites_counter = self.browser.find_element(*HeaderLocators.FAVORITES_COUNTER)        
        if favorites_counter.text == amount:
            return True
        else: 
            return False    

    # check that the element is clickable
    def is_element_clickable(self, how, what):
        try:
            element = self.browser.find_element(how, what)
            element.click()
        except (ElementClickInterceptedException, ElementNotInteractableException):
            return False
        return True    

    # check that the element is present on the page
    def is_element_present(self, how, what):
        try:
            self.browser.find_element(how, what)
        except NoSuchElementException:
            return False
        return True

    def is_favorites_page_icon_has_not_counter(self):
        return not self.is_element_present(*HeaderLocators.FAVORITES_COUNTER)    
    
    # open page
    def open(self):
        self.browser.get(self.url)        

    # check that login link is present on the page
    def should_be_login_link(self):
        assert self.is_element_present(*HeaderLocators.LOGIN_LINK), "Login link is not presented"    
    
    def sort_by(self, criterion: Literal['price', 'rating'], direction: Literal['high', 'low']):
        sort_dropdown = self.browser.find_element(*BasePageLocators.SORT_DROPDOWN)
        sort_dropdown.click()

        if criterion == 'price' and direction == 'high':
            sort_button = self.browser.find_element(*BasePageLocators.SORT_PRICE_HIGH)
        elif criterion == 'price' and direction == 'low':
            sort_button = self.browser.find_element(*BasePageLocators.SORT_PRICE_LOW)            
        elif criterion == 'rating' and direction == 'high':
            sort_button = self.browser.find_element(*BasePageLocators.SORT_RATING_HIGH)
        elif criterion == 'rating' and direction == 'low':
            sort_button = self.browser.find_element(*BasePageLocators.SORT_RATING_LOW)
        else:
            raise ValueError('Sort criterion must be "price" or "rating" \
                            and sort direction must be "high" or "low"')
        
        sort_button.click()
        