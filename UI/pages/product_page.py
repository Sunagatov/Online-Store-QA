import re

from .base_page import BasePage
from .locators import ProductPageLocators, HeaderLocators


class ProductPage(BasePage):
    def add_product_to_cart(self):
        add_to_cart_button = self.browser.find_element(*ProductPageLocators.ADD_TO_CART_BUTTON)
        add_to_cart_button.click()
    
    def add_product_to_favorites(self):
        add_to_favorites_button = self.browser.find_element(*ProductPageLocators.ADD_TO_FAVORITES_BUTTON)
        add_to_favorites_button.click()
    
    def click_minus_button(self):
        minus_button = self.browser.find_element(*ProductPageLocators.MINUS_BUTTON) 
        minus_button.click()        
    
    def click_plus_button(self):
        plus_button = self.browser.find_element(*ProductPageLocators.PLUS_BUTTON)
        plus_button.click()

    def get_product_name(self):
        return self.browser.find_element(*ProductPageLocators.PRODUCT_NAME).text
    
    def get_product_price(self):
        product_price_element = self.browser.find_element(*ProductPageLocators.ADD_TO_CART_BUTTON).text
        pattern = r"[0-9.]"
        product_price = re.findall(pattern, product_price_element)
        return float("".join(product_price))
        
    def get_product_rating(self):
        product_rating = self.browser.find_element(*ProductPageLocators.PRODUCT_RATING).text
        return product_rating
    
    def get_product_reviews(self):
        product_reviews_element = self.browser.find_element(*ProductPageLocators.PRODUCT_REVIEWS).text
        pattern = re.compile(r'\b\d+\b')
        product_reviews = pattern.findall(product_reviews_element)
        return product_reviews[0]
    
    def get_product_weight(self):
        product_weight_element = self.browser.find_element(*ProductPageLocators.PRODUCT_WEIGHT).text
        pattern = re.compile(r'\b\d+\b')
        product_weight = pattern.findall(product_weight_element)
        return product_weight[0]
    
    def is_cart_page_link_present(self):
        return self.is_element_present(*HeaderLocators.CART_LINK)

    def is_cart_page_link_clickable(self):
        return self.is_element_clickable(*HeaderLocators.CART_LINK)    
    
    # check that amount changed after click "Plus" or "Minus"
    def is_change_amount(self, amount):
        amount_element = self.browser.find_element(*ProductPageLocators.AMOUNT)
        if amount_element.text == amount:
            return True
        else: 
            return False

    def is_favorites_page_link_present(self):
        return self.is_element_present(*HeaderLocators.FAVORITES_PAGE_LINK)

    def is_favorites_page_link_clickable(self):
        return self.is_element_clickable(*HeaderLocators.FAVORITES_PAGE_LINK)   

    def is_heart_red(self):
        heart_image = self.browser.find_element(*ProductPageLocators.RED_HEART_IMAGE)
        # check that red heart image is present on favorite button
        if heart_image.get_attribute('src') == 'https://iced-latte.uk/_next/static/media/active_heart.06676f62.svg':
            return True
        else:
            return False
    
    def is_heart_transparent(self):
        heart_image = self.browser.find_element(*ProductPageLocators.TRANSPARENT_HEART_IMAGE)
        # check that transparent heart image is present on favorite button
        if heart_image.get_attribute('src') == 'https://iced-latte.uk/_next/static/media/not_active_heart.49e56974.svg':
            return True
        else:
            return False

    def is_login_page_link_present(self):
        return self.is_element_present(*HeaderLocators.LOGIN_LINK)

    def is_login_page_link_clickable(self):
        return self.is_element_clickable(*HeaderLocators.LOGIN_LINK)
    
    def is_main_page_link_present(self):
        return self.is_element_present(*HeaderLocators.MAIN_PAGE_LINK)
    
    def is_main_page_link_clickable(self):
        return self.is_element_clickable(*HeaderLocators.MAIN_PAGE_LINK)

    def is_profile_page_link_present(self):
        return self.is_element_present(*HeaderLocators.PROFILE_LINK)
    
    def is_profile_page_link_clickable(self):
        return self.is_element_clickable(*HeaderLocators.PROFILE_LINK)

    def remove_product_from_favorites(self):
        remove_from_favorites_button = self.browser.find_element(*ProductPageLocators.REMOVE_FROM_FAVORITES_BUTTON)
        remove_from_favorites_button.click()
    