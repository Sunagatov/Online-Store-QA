from allure import step, title, severity, story, severity_level
# import pytest
from time import sleep

from .pages.BasePage import BasePage
from .pages.FavoritesPage import FavoritesPage
from .pages.LoginPage import LoginPage
from .configs import link, login_page_link
from .set_of_steps import login_user, remove_products_from_cart_and_favorites


@story("Favorites")
@title("Test for favorites")
# @allure.description("")
# @allure.tag("")
@severity(severity_level.NORMAL)
class TestFavorites:
    # -------------- USER----------------
    @title("User. Check adding product to favorites and removing from favorites from products catalog")
    def test_user_add_remove_favorites_from_catalog_user(self, browser):
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
            assert main_page.is_heart_on_product_transparent(), 'Heart on product card is not transparent'
        with step('Check that favorites counter on header is not present'):
            assert main_page.is_favorites_page_icon_has_not_counter(), 'Favorites counter is present'

    @title("User. Check removing product from favorites on favorites page")
    def test_user_remove_product_on_favorites_page(self, browser):
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

    @title('User. Test "Continue Shopping" button on empty favorites page')
    def test_user_continue_shopping_button(self, browser):
        login_user(browser, link)
        sleep(2)  # waiting is mandatory (do not remove)
        remove_products_from_cart_and_favorites(browser, link)

        main_page = BasePage(browser, link)
        main_page.go_to_favorites_page()
        favorites_page = FavoritesPage(browser, browser.current_url)

        favorites_page.click_continue_shopping_button()

        main_page = BasePage(browser, link)
        with step('Check that main page is presented'):
            assert main_page.is_correct_page_presented(link), 'Main page is not presented'

# -------------- GUEST ----------------
    @title("Guest. Check adding product to favorites and removing from favorites from products catalog")
    def test_guest_add_remove_favorites_from_catalog(self, browser):
        main_page = BasePage(browser, link)
        main_page.open()
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
            assert main_page.is_heart_on_product_transparent(), 'Heart on product card is not transparent'
        with step('Check that favorites counter on header is not present'):
            assert main_page.is_favorites_page_icon_has_not_counter(), 'Favorites counter is present'

    @title("Guest. Check removing product from favorites on favorites page")
    def test_guest_remove_product_on_favorites_page(self, browser):
        main_page = BasePage(browser, link)
        main_page.open()
        main_page.add_product_to_favorites()

        main_page.go_to_favorites_page()
        favorites_page = FavoritesPage(browser, browser.current_url)
        favorites_page.remove_favorites_products()

        with step('Check that empty favorites message is present'):
            assert favorites_page.is_favorites_empty(), 'Favorites list is not empty'

    @title('Guest. Test "Continue Shopping" and "Log in" button on empty favorites page')
    def test_guest_empty_favorites_buttons(self, browser):
        main_page = BasePage(browser, link)
        main_page.open()
        main_page.go_to_favorites_page()
        favorites_page = FavoritesPage(browser, browser.current_url)

        favorites_page.click_continue_shopping_button()

        main_page = BasePage(browser, link)
        with step('Check that main page is presented'):
            assert main_page.is_correct_page_presented(link), 'Main page is not presented'

        main_page.go_to_favorites_page()
        favorites_page = FavoritesPage(browser, browser.current_url)

        favorites_page.click_log_in_button()

        login_page = LoginPage(browser, browser.current_url)
        with step('Check that login page is presented'):
            assert login_page.is_correct_page_presented(login_page_link), 'Login page is not presented'
