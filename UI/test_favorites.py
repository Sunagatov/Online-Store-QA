from allure import step, title, severity, story, severity_level
# import pytest
from time import sleep

from .pages.base_page import BasePage
from .pages.favorites_page import FavoritesPage
from .configs import link
from .set_of_steps import login_user, remove_products_from_cart_and_favorites


@story("Favorites")
@title("Test for favorites")
# @allure.description("")
# @allure.tag("")
@severity(severity_level.NORMAL)
class TestFavorites:
    # -------------- USER----------------
    @title("Check adding product to favorites and removing from favorites from products catalog")
    def test_add_remove_favorites_from_catalog(self, browser):
        login_user(browser, link)
        sleep(2)  # waiting is mandatory (do not remove)
        remove_products_from_cart_and_favorites(browser, link)

        main_page = BasePage(browser, link)
        product_name = main_page.get_product_name()
        main_page.add_product_to_favorites()

        with step('Check the heart on the product card is red'):
            assert main_page.is_heart_on_product_red(), 'Heart on product card is not red'
        with step('Check that favorites counter on header is increase'):
            assert main_page.is_change_favorites_counter('1'), 'Favorites counter on header is not increase'

        main_page.go_to_favorites_page()
        favorites_page = FavoritesPage(browser, browser.current_url)

        with step('Check there is the product in favorites'):
            assert favorites_page.is_product_in_favorites(product_name), 'There is not product in favorites'

        favorites_page.go_to_main_page()
        main_page = BasePage(browser, link)
        main_page.remove_product_from_favorites()

        with step('Check the heart on the product card is transparent'):
            main_page.is_heart_on_product_transparent(), 'Heart on product card is not transparent'
        with step('Check that favorites counter on header is not present'):
            main_page.is_favorites_page_icon_has_not_counter(), 'Favorites counter is present'

    @title("Check removing product from favorites on favorites page")
    def test_remove_product_on_favorites_page(self, browser):
        login_user(browser, link)
        sleep(2)  # waiting is mandatory (do not remove)
        remove_products_from_cart_and_favorites(browser, link)

        main_page = BasePage(browser, link)
        main_page.add_product_to_favorites()

        main_page.go_to_favorites_page()
        favorites_page = FavoritesPage(browser, browser.current_url)
        favorites_page.remove_favorites_products()

        with step('Check that empty favorites message is present'):
            assert favorites_page.is_favorites_empty(), 'Favorites list is not empty'
