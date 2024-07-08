import re

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from .base_page import BasePage
from .locators import ProductPageLocators, HeaderLocators


class ProductPage(BasePage):
    def add_product_to_cart(self):
        add_to_cart_button = self.browser.find_element(*ProductPageLocators.ADD_TO_CART_BUTTON)
        add_to_cart_button.click()
    
    def add_product_to_favorites(self):
        add_to_favorites_button = self.browser.find_element(*ProductPageLocators.ADD_TO_FAVORITES_BUTTON)
        add_to_favorites_button.click() 
    
    def rating_checkbox(self, rating):
        product_page_locators = ProductPageLocators()
        locator = product_page_locators.checkbox(rating)
        rating_checkbox = self.browser.find_element(*locator)
        rating_checkbox.click()
        
    def click_add_review(self):
        add_review_button = self.browser.find_element(*ProductPageLocators.ADD_REVIEW_BUTTON)
        add_review_button.click()
    
    def click_minus_button(self):
        minus_button = self.browser.find_element(*ProductPageLocators.MINUS_BUTTON) 
        minus_button.click()        
    
    def click_plus_button(self):
        plus_button = self.browser.find_element(*ProductPageLocators.PLUS_BUTTON)
        plus_button.click()    

    def delete_review(self):
        delete_review_button = self.browser.find_elements(*ProductPageLocators.DELETE_REVIEW_BUTTON)
        for del_btn in delete_review_button:
            del_btn.click()
            WebDriverWait(self.browser, 4).until_not(
                ec.presence_of_element_located(ProductPageLocators.REVIEW_AUTHOR)
            )

    def dislike_own_review(self):
        dislike_counter_before = self.browser.find_element(*ProductPageLocators.DISLIKE_OWN_COUNTER).text
        dislike_button = self.browser.find_element(*ProductPageLocators.DISLIKE_OWN_BUTTON)    
        dislike_button.click()        
        WebDriverWait(self.browser, 4).until(
            lambda driver: driver.find_element(*ProductPageLocators.DISLIKE_OWN_COUNTER).text 
            != dislike_counter_before
        )

    def dislike_someone_review(self):
        dislike_counter_before = self.browser.find_element(*ProductPageLocators.DISLIKE_SOMEONE_COUNTER).text
        dislike_button = self.browser.find_element(*ProductPageLocators.DISLIKE_SOMEONE_BUTTON)    
        dislike_button.click()        
        WebDriverWait(self.browser, 5).until(
            lambda driver: driver.find_element(*ProductPageLocators.DISLIKE_SOMEONE_COUNTER).text 
            != dislike_counter_before
        )

    def fill_review(self, review_text):
        review_field = self.browser.find_element(*ProductPageLocators.REVIEW_FIELD)
        review_field.send_keys(review_text)

    def get_actual_rating(self):
        # check is no rating product
        product_rating_text = self.browser.find_element(*ProductPageLocators.PRODUCT_RATING).text
        if product_rating_text == 'No rating':
            print('No Rating')
            return 0, 0
        else:
            # get the number of reviews corresponding to each rating
            star_5_element = self.browser.find_element(*ProductPageLocators.STAR_5)
            star_4_element = self.browser.find_element(*ProductPageLocators.STAR_4)
            star_3_element = self.browser.find_element(*ProductPageLocators.STAR_3)
            star_2_element = self.browser.find_element(*ProductPageLocators.STAR_2)
            star_1_element = self.browser.find_element(*ProductPageLocators.STAR_1)

            star_5_review_amount = int(star_5_element.text[:-8])
            star_4_review_amount = int(star_4_element.text[:-8])
            star_3_review_amount = int(star_3_element.text[:-8])
            star_2_review_amount = int(star_2_element.text[:-8])
            star_1_review_amount = int(star_1_element.text[:-8])

            star_sum = (
                star_5_review_amount * 5
                + star_4_review_amount * 4
                + star_3_review_amount * 3
                + star_2_review_amount * 2
                + star_1_review_amount * 1
            ) 
            review_amount = (
                star_5_review_amount
                + star_4_review_amount
                + star_3_review_amount
                + star_2_review_amount
                + star_1_review_amount
            )
            actual_rating = round(star_sum / review_amount, 1)
            print('actual_rating, review_amount', actual_rating, review_amount)
            return actual_rating, review_amount

    def get_dislike_own_counter(self):
        dislike_counter = self.browser.find_element(*ProductPageLocators.DISLIKE_OWN_COUNTER)
        return int(dislike_counter.text)

    def get_dislike_someone_counter(self):
        dislike_counter = self.browser.find_element(*ProductPageLocators.DISLIKE_SOMEONE_COUNTER)
        return int(dislike_counter.text)
    
    def get_like_own_counter(self):
        like_counter = self.browser.find_element(*ProductPageLocators.LIKE_OWN_COUNTER)
        return int(like_counter.text)
    
    def get_like_someone_counter(self):
        like_counter = self.browser.find_element(*ProductPageLocators.LIKE_SOMEONE_COUNTER)
        return int(like_counter.text)

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
    
    def get_review_author(self):
        review_author = WebDriverWait(self.browser, 4).until(
            ec.presence_of_element_located(ProductPageLocators.REVIEW_AUTHOR)
        )
        return review_author.text
    
    # This amount: "Based on X reviews"
    def get_reviews_amount(self):
        if self.is_element_present(*ProductPageLocators.REVIEWS_AMOUNT):
            reviews_amount_element = self.browser.find_element(*ProductPageLocators.REVIEWS_AMOUNT).text
            pattern = re.compile(r'\b\d+\b')
            reviews_amount = pattern.findall(reviews_amount_element)
            return int(reviews_amount[0])
        else:
            return 0
        
    def get_review_symbols_counter(self):
        counter = self.browser.find_element(*ProductPageLocators.REVIEW_SYMBOLS_COUNTER).text        
        return int(counter[:-5])
    
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
    
    def is_only_filtered_ratings(self, ratings):
        is_only_filtered_ratings = True
        # get all ratings from filtered reviews list
        filtered_ratings = self.browser.find_elements(*ProductPageLocators.RATINGS_IN_REVIEWS_LIST)
        
        for filtered_rating in filtered_ratings:            
            if filtered_rating.text not in ratings:
                is_only_filtered_ratings = False
        
        return is_only_filtered_ratings

    def is_profile_page_link_present(self):
        return self.is_element_present(*HeaderLocators.PROFILE_LINK)
    
    def is_profile_page_link_clickable(self):
        return self.is_element_clickable(*HeaderLocators.PROFILE_LINK)
    
    def is_submit_button_not_active(self):
        submit_review_button = self.browser.find_element(*ProductPageLocators.SUBMIT_REVIEW_BUTTON)
        return False if submit_review_button.is_enabled() else True

    def like_own_review(self):
        like_counter_before = self.browser.find_element(*ProductPageLocators.LIKE_OWN_COUNTER).text
        like_button = self.browser.find_element(*ProductPageLocators.LIKE_OWN_BUTTON)            
        like_button.click()                
        WebDriverWait(self.browser, 4).until(
            lambda driver: driver.find_element(*ProductPageLocators.LIKE_OWN_COUNTER).text != like_counter_before
        )

    def like_someone_review(self):
        like_counter_before = self.browser.find_element(*ProductPageLocators.LIKE_SOMEONE_COUNTER).text
        like_button = self.browser.find_element(*ProductPageLocators.LIKE_SOMEONE_BUTTON)            
        like_button.click()                
        WebDriverWait(self.browser, 5).until(
            lambda driver: driver.find_element(*ProductPageLocators.LIKE_SOMEONE_COUNTER).text != like_counter_before
        )    

    def remove_product_from_favorites(self):
        remove_from_favorites_button = self.browser.find_element(*ProductPageLocators.REMOVE_FROM_FAVORITES_BUTTON)
        remove_from_favorites_button.click()

    def set_rating(self):
        # set 2-star rating
        star_button_2 = self.browser.find_element(*ProductPageLocators.STAR_BUTTON_2)
        star_button_2.click()  
    
    def submit_review(self):
        submit_review_button = self.browser.find_element(*ProductPageLocators.SUBMIT_REVIEW_BUTTON)
        submit_review_button.click()
        