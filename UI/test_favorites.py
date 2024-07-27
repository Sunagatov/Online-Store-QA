from allure import step, title, severity, story, severity_level
import pytest
from time import sleep

from .pages.base_page import BasePage
from .configs import link
from set_of_steps import login_user, remove_products_from_cart_and_favorites


@story("Favorites")
@title("Test for favorites")
# @allure.description("")
# @allure.tag("")
@severity(severity_level.NORMAL)
class TestFavorites:
    @title("Check adding product to favorites")
    def test_add_product_to_favorites(self, browser):
        login_user(browser, link)
        sleep(2)  # waiting is mandatory (do not remove)
        remove_products_from_cart_and_favorites(browser, link)
