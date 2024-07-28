from allure import step
from time import sleep
from .base_page import BasePage
from .locators import FavoritesPageLocators


class FavoritesPage(BasePage):
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
