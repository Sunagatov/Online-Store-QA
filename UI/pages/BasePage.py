import re
from allure import step
from typing import Literal
from time import sleep

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, \
                                       ElementClickInterceptedException, \
                                       ElementNotInteractableException

from .locators import BasePageLocators, HeaderLocators


class BasePage:

    def __init__(self, browser: WebDriver, url: str, timeout: int = 4):
        self.browser = browser
        self.url = url
        self.browser.implicitly_wait(timeout)  # turn on implicitly wait  
        self.browser.maximize_window()
    
    @step('Add product to cart')
    def add_product_to_cart(self) -> None:
        button = self.browser.find_element(*BasePageLocators.ADD_TO_CART_BUTTON)
        button.click()
    
    def add_product_2_to_cart(self):
        button = self.browser.find_element(*BasePageLocators.ADD_TO_CART_BUTTON_2)
        button.click()

    @step('Add product to favorites')
    def add_product_to_favorites(self) -> None:
        add_to_favorites_button = self.browser.find_element(*BasePageLocators.ADD_TO_FAVORITES_BUTTON)
        add_to_favorites_button.click()

    @step('Click "By default" button')
    def by_default(self) -> None:
        by_default_button = self.browser.find_element(*BasePageLocators.BY_DEFAULT_BUTTON)
        by_default_button.click()

    @step('Click minus button')
    def click_minus_button(self) -> None:
        minus_button = self.browser.find_element(*BasePageLocators.MINUS_BUTTON)
        minus_button.click()
        sleep(2)  # waiting is mandatory (do not remove)
    
    @step('Click plus button')
    def click_plus_button(self) -> None:
        plus_button = self.browser.find_element(*BasePageLocators.PLUS_BUTTON)
        plus_button.click()
        sleep(2)  # waiting is mandatory (do not remove)

    @step('Filter products in catalog by brand')
    def filter_products_by_brand(self, brand: str) -> None:
        base_page_locators = BasePageLocators()
        brand_checkbox_locator = base_page_locators.brand_checkbox(brand)
        brand_checkbox = self.browser.find_element(*brand_checkbox_locator)
        brand_checkbox.click()

    @step('Filter products in catalog by price')
    def filter_products_by_price(self, price_from: str, price_to: str) -> None:
        price_from_field = self.browser.find_element(*BasePageLocators.PRICE_FROM_FIELD)
        price_from_field.send_keys(price_from)

        price_to_field = self.browser.find_element(*BasePageLocators.PRICE_TO_FIELD)
        price_to_field.send_keys(price_to)

    @step('Filter products in catalog by rating')
    def filter_products_by_rating(self, rating: Literal['4', '3', '2', '1', 'any']) -> None:
        base_page_locators = BasePageLocators()
        rating_checkbox_locator = base_page_locators.rating_checkbox(rating)
        rating_checkbox = self.browser.find_element(*rating_checkbox_locator)
        rating_checkbox.click()

    @step('Filter products in catalog by seller')
    def filter_products_by_seller(self, seller: str) -> None:
        base_page_locators = BasePageLocators()
        seller_checkbox_locator = base_page_locators.seller_checkbox(seller)
        seller_checkbox = self.browser.find_element(*seller_checkbox_locator)
        # scroll page down
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        seller_checkbox.click()

    @step('Get brand list length')
    def get_brand_list_length(self) -> int:
        brand_list = self.browser.find_elements(*BasePageLocators.BRAND_LIST)
        return len(brand_list)

    @step('Get products list length')
    def get_products_list_length(self) -> int:
        while self.is_element_present(*BasePageLocators.SHOW_MORE_BUTTON):
            show_more_button = self.browser.find_element(*BasePageLocators.SHOW_MORE_BUTTON)
            show_more_button.click()

        products_list = self.browser.find_elements(*BasePageLocators.PRODUCTS_LIST)
        return len(products_list)

    def get_product_name(self) -> str:
        return self.browser.find_element(*BasePageLocators.PRODUCT_NAME).text
    
    def get_product_price(self):
        product_price_element = self.browser.find_element(*BasePageLocators.PRODUCT_PRICE).text
        return float(product_price_element[1:])

    def get_products_price_list(self) -> list:
        products_price_elements = self.browser.find_elements(*BasePageLocators.PRODUCT_PRICE_LIST)
        products_price_list = []

        for product_price_element in products_price_elements:
            products_price_list.append(float(product_price_element.text[1:]))

        return products_price_list

    def get_product_rating(self):
        product_rating = self.browser.find_element(*BasePageLocators.PRODUCT_RATING).text
        return product_rating

    def get_products_rating_list(self) -> list:
        products_rating_elements = self.browser.find_elements(*BasePageLocators.PRODUCTS_RATING_LIST)
        products_rating_list = []

        for product_rating_element in products_rating_elements:
            products_rating_list.append(float(product_rating_element.text))

        return products_rating_list
    
    def get_product_reviews(self):
        product_reviews_element = self.browser.find_element(*BasePageLocators.PRODUCT_REVIEWS).text
        pattern = re.compile(r'\b\d+\b')
        product_reviews = pattern.findall(product_reviews_element)
        return product_reviews[0]

    @step('Get seller list length')
    def get_seller_list_length(self) -> int:
        seller_list = self.browser.find_elements(*BasePageLocators.SELLER_LIST)
        return len(seller_list)

    @step('Go to Cart Page')
    def go_to_cart_page(self) -> None:
        link = self.browser.find_element(*HeaderLocators.CART_LINK)
        link.click()
    
    @step('Go to favorites page')
    def go_to_favorites_page(self):
        link = self.browser.find_element(*HeaderLocators.FAVORITES_PAGE_LINK)
        link.click()

    def go_to_login_page(self):
        link = self.browser.find_element(*HeaderLocators.LOGIN_LINK)
        link.click()

    @step('Go to main page')
    def go_to_main_page(self):
        main_page_link = self.browser.find_element(*HeaderLocators.MAIN_PAGE_LINK)
        main_page_link.click()

    def go_to_product_page(self):
        link = self.browser.find_element(*BasePageLocators.PRODUCT_LINK)
        link.click()

    def go_to_profile_page(self):        
        link = self.browser.find_element(*HeaderLocators.PROFILE_LINK)
        link.click()

    def is_add_to_cart_button_present(self) -> bool:
        return self.is_element_present(*BasePageLocators.ADD_TO_CART_BUTTON)

    def is_badge_present(self, product_filter: str) -> bool:
        base_page_locators = BasePageLocators()
        return self.is_element_present(*base_page_locators.remove_filter_badge(product_filter))

    def is_cart_counter_present(self) -> bool:
        return self.is_element_present(*HeaderLocators.CART_COUNTER)

    # check that amount on cart icon changed after adding product to cart 
    # and click "Plus" or "Minus"
    def is_change_cart_counter(self, amount: str) -> bool:
        cart_counter = self.browser.find_element(*HeaderLocators.CART_COUNTER)
        if cart_counter.text == amount:
            return True
        else: 
            return False

    # check that amount on favorites page icon changed
    def is_change_favorites_counter(self, amount: str) -> bool:
        favorites_counter = self.browser.find_element(*HeaderLocators.FAVORITES_COUNTER)        
        if favorites_counter.text == amount:
            return True
        else: 
            return False

    def is_change_product_counter(self, amount: str) -> bool:
        product_counter = self.browser.find_element(*BasePageLocators.PRODUCT_COUNTER)
        if product_counter.text == amount:
            return True
        else: 
            return False

    def is_correct_page_presented(self, url: str) -> bool:
        now_url = self.browser.current_url

        if now_url == url:
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
    def is_element_present(self, how, what) -> bool:
        try:
            self.browser.find_element(how, what)
        except NoSuchElementException:
            return False
        return True

    def is_favorites_page_icon_has_not_counter(self):
        return not self.is_element_present(*HeaderLocators.FAVORITES_COUNTER)

    def is_filtering_by_brand_correct(self, brand: str) -> bool:
        while self.is_element_present(*BasePageLocators.SHOW_MORE_BUTTON):
            show_more_button = self.browser.find_element(*BasePageLocators.SHOW_MORE_BUTTON)
            show_more_button.click()

        products_brands_list = self.browser.find_elements(*BasePageLocators.PRODUCTS_BRANDS_LIST)
        for product_brand in products_brands_list:
            if product_brand.text != f'by {brand}':
                return False

        return True

    def is_filtering_by_price_correct(self, price_from: str, price_to: str) -> bool:
        while self.is_element_present(*BasePageLocators.SHOW_MORE_BUTTON):
            show_more_button = self.browser.find_element(*BasePageLocators.SHOW_MORE_BUTTON)
            show_more_button.click()

        # create filtered products price list
        products_price_list = self.get_products_price_list()
        print('\n', products_price_list)
        for product_price in products_price_list:
            if float(product_price) <= float(price_from) or float(product_price) >= float(price_to):
                return False
        return True

    def is_filtering_by_rating_correct(self, rating: Literal['4', '3', '2', '1', 'any']) -> bool:
        while self.is_element_present(*BasePageLocators.SHOW_MORE_BUTTON):
            show_more_button = self.browser.find_element(*BasePageLocators.SHOW_MORE_BUTTON)
            show_more_button.click()

        if rating in ['4', '3', '2', '1']:
            # create products rating list
            products_rating_list = self.get_products_rating_list()
            print('\n', products_rating_list)

            for product_rating in products_rating_list:
                if product_rating < float(rating):
                    return False
        else:
            products_with_rating_list = self.browser.find_elements(*BasePageLocators.PRODUCTS_RATING_LIST)
            products_no_rating_list = self.browser.find_elements(*BasePageLocators.PRODUCTS_NO_RATING_LIST)
            products_list = self.browser.find_elements(*BasePageLocators.PRODUCTS_LIST)
            if len(products_list) != len(products_with_rating_list) + len(products_no_rating_list):
                return False

        return True

    def is_filtering_by_seller_correct(self, seller: str) -> bool:
        while self.is_element_present(*BasePageLocators.SHOW_MORE_BUTTON):
            show_more_button = self.browser.find_element(*BasePageLocators.SHOW_MORE_BUTTON)
            show_more_button.click()

        products_sellers_list = self.browser.find_elements(*BasePageLocators.PRODUCTS_SELLERS_LIST)
        for product_seller in products_sellers_list:
            if product_seller.text != seller:
                return False

        return True

    def is_heart_on_product_red(self) -> bool:
        return self.is_element_present(*BasePageLocators.HEART_LIKED_ICON)

    def is_heart_on_product_transparent(self) -> bool:
        return self.is_element_present(*BasePageLocators.HEART_UNLIKED_ICON)

    def is_sorting_correct(self, criterion: Literal['price', 'rating'], direction: Literal['high', 'low']) -> bool:
        while self.is_element_present(*BasePageLocators.SHOW_MORE_BUTTON):
            show_more_button = self.browser.find_element(*BasePageLocators.SHOW_MORE_BUTTON)
            show_more_button.click()

        # create products rating list
        products_rating_list = self.get_products_rating_list()
        print('\n', products_rating_list)

        # create products price list
        products_price_list = self.get_products_price_list()
        print('\n', products_price_list)

        if criterion == 'rating' and direction == 'high':
            for i in range(len(products_rating_list)-1):
                if products_rating_list[i] < products_rating_list[i+1]:
                    return False
        elif criterion == 'rating' and direction == 'low':
            for i in range(len(products_rating_list) - 1):
                if products_rating_list[i] > products_rating_list[i + 1]:
                    return False
        elif criterion == 'price' and direction == 'high':
            for i in range(len(products_rating_list) - 1):
                if products_price_list[i] < products_price_list[i + 1]:
                    return False
        elif criterion == 'price' and direction == 'low':
            for i in range(len(products_rating_list) - 1):
                if products_price_list[i] > products_price_list[i + 1]:
                    return False
        else:
            raise ValueError('Sort criterion must be "price" or "rating" \
                            and sort direction must be "high" or "low"')

        return True

    @step('Open main page')
    def open(self) -> None:
        self.browser.get(self.url)        

    @step('Click cross on the badge to remove filter')
    def remove_filter(self, products_filter: str):
        base_page_locator = BasePageLocators()
        remove_filter_badge_locator = base_page_locator.remove_filter_badge(products_filter)
        remove_filter_badge = self.browser.find_element(*remove_filter_badge_locator)
        remove_filter_badge.click()

    @step('Remove product from favorites')
    def remove_product_from_favorites(self) -> None:
        remove_from_favorites_button = self.browser.find_element(*BasePageLocators.REMOVE_FROM_FAVORITES_BUTTON)
        remove_from_favorites_button.click()

    # check that login link is present on the page
    def should_be_login_link(self):
        assert self.is_element_present(*HeaderLocators.LOGIN_LINK), "Login link is not presented"    

    @step('Click show more/less brand button')
    def show_more_less_brand(self):
        show_more_less_brand_button = self.browser.find_element(*BasePageLocators.SHOW_MORE_LESS_BRAND_BUTTON)
        # scroll page down
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        show_more_less_brand_button.click()

    @step('Click show more/less seller button')
    def show_more_less_seller(self):
        show_more_less_seller_button = self.browser.find_element(*BasePageLocators.SHOW_MORE_LESS_SELLER_BUTTON)
        # scroll page down
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        show_more_less_seller_button.click()

    @step('Sort product catalog')
    def sort_by(self, criterion: Literal['price', 'rating'], direction: Literal['high', 'low']) -> None:
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
        