from allure import step
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from .base_page import BasePage
from .locators import FavoritesPageLocators, BasePageLocators, LoginPageLocators
from ..configs import login_page_link


class FavoritesPage(BasePage):
    @step('Click "Continue Shopping" button')
    def click_continue_shopping_button(self) -> None:
        continue_shopping_button = self.browser.find_element(*FavoritesPageLocators.CONTINUE_SHOPPING_BUTTON)
        continue_shopping_button.click()

        # waiting for the main page to load
        WebDriverWait(self.browser, 4).until(ec.presence_of_element_located(BasePageLocators.HEADING_ELEMENT))

    @step('Click "Log in" button')
    def click_log_in_button(self) -> None:
        log_in_button = self.browser.find_element(*FavoritesPageLocators.LOG_IN_BUTTON)
        log_in_button.click()

        # waiting for the login page to load
        WebDriverWait(self.browser, 4).until(ec.url_to_be(login_page_link))

    def go_to_product_page(self) -> None:
        link = self.browser.find_element(*FavoritesPageLocators.PRODUCT_LINK)
        link.click()

    def is_favorites_empty(self) -> bool:
        return self.is_element_present(*FavoritesPageLocators.EMPTY_FAVORITES_MESSAGE)

    def is_product_in_favorites(self, product_name: str) -> bool:
        favorites_page_product_name = self.browser.find_element(*FavoritesPageLocators.PRODUCT_NAME)
        if favorites_page_product_name.text == product_name:
            return True
        else: 
            return False
    
    @step('Remove products from favorites')
    def remove_favorites_products(self) -> None:
        buttons = self.browser.find_elements(*FavoritesPageLocators.UNLIKE_BUTTONS)
        for button in buttons:
            button.click()
            sleep(2)  # waiting is mandatory (do not remove)
