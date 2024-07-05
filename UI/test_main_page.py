from allure import step, title, severity, story, severity_level
# import pytest
from time import sleep

from .pages.base_page import BasePage
from .configs import link


@story("Product Catalog")
@title("Test for Main Page")
# @allure.description("")
# @allure.tag("")
@severity(severity_level.CRITICAL)
class TestMainPage:
    @title("Check sort products by high rating on main page")
    def test_sort_products_by_high_rating(self, browser):
        main_page = BasePage(browser, link)
        main_page.open()
        main_page.sort_by('rating', 'high')

        with step('Check that the sorting is correct'):
            assert main_page.is_sorting_correct('rating', 'high'), 'The sorting is not correct'

    @title("Check sort products by low rating on main page")
    def test_sort_products_by_low_rating(self, browser):
        main_page = BasePage(browser, link)
        main_page.open()
        main_page.sort_by('rating', 'low')

        with step('Check that the sorting is correct'):
            assert main_page.is_sorting_correct('rating', 'low'), 'The sorting is not correct'

    @title("Check sort products by high price on main page")
    def test_sort_products_by_high_price(self, browser):
        main_page = BasePage(browser, link)
        main_page.open()
        main_page.sort_by('price', 'high')

        with step('Check that the sorting is correct'):
            assert main_page.is_sorting_correct('price', 'high'), 'The sorting is not correct'

    @title("Check sort products by low price on main page")
    def test_sort_products_by_low_price(self, browser):
        main_page = BasePage(browser, link)
        main_page.open()
        main_page.sort_by('price', 'low')

        with step('Check that the sorting is correct'):
            assert main_page.is_sorting_correct('price', 'low'), 'The sorting is not correct'

    @title("Check filter products by price on main page")
    def test_filter_products_by_price(self, browser):
        main_page = BasePage(browser, link)
        main_page.open()
        price_from = '4'
        price_to = '5.5'
        main_page.filter_products_by_price(price_from, price_to)
        sleep(5)

        with step('Check that filtering by price is correct'):
            assert main_page.is_filtering_by_price_correct(price_from, price_to), 'The filtering is not correct'
