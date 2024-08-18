from allure import step, title, severity, story, severity_level
import pytest
import re
# from time import sleep

from .pages.BasePage import BasePage
from .configs import link


@story("Product Catalog")
@title("Negative Test for Main Page")
# @allure.description("")
# @allure.tag("")
@severity(severity_level.NORMAL)
class TestMainPageNegative:
    @title("Check filter products by 'price from' (digits with other symbols) on main page")
    @pytest.mark.xfail(reason='Bug is not fixed', run=True)
    @pytest.mark.parametrize("price", ('-4', '4-', 'a4', '4a', '4,4', ' 4', '4 ', '4 4'))
    def test_filter_products_by_price_from_digits(self, browser, price):
        main_page = BasePage(browser, link)
        main_page.open()
        price_from = price
        price_to = '1000'

        main_page.filter_products_by_price(price_from, price_to)

        # remove all non-digit symbols from price
        price_from_after_processing = re.sub(r'\D', '', price_from)

        with step('Check that filtering by price is correct'):
            assert main_page.is_filtering_by_price_correct(price_from_after_processing, price_to), \
                'The filtering is not correct'

    @title("Check filter products by 'price to' (digits with other symbols) on main page")
    @pytest.mark.xfail(reason='Bug is not fixed', run=True)
    @pytest.mark.parametrize("price", ('-4', '4-', 'a4', '4a', '4,4', ' 4', '4 ', '4 4'))
    def test_filter_products_by_price_to_digits(self, browser, price):
        main_page = BasePage(browser, link)
        main_page.open()
        price_from = '0'
        price_to = price

        main_page.filter_products_by_price(price_from, price_to)

        # remove all non-digit symbols from price
        price_to_after_processing = re.sub(r'\D', '', price_to)

        with step('Check that filtering by price is correct'):
            assert main_page.is_filtering_by_price_correct(price_from, price_to_after_processing), \
                'The filtering is not correct'

    @title("Check filter products by 'price from' (symbols without digits) on main page")
    @pytest.mark.parametrize("price", ('-', ',', '!!', 'abc'))
    def test_filter_products_by_price_from(self, browser, price):
        main_page = BasePage(browser, link)
        main_page.open()
        price_from = price
        price_to = '1000'

        main_page.filter_products_by_price(price_from, price_to)

        with step('Check that filtering by price is correct'):
            assert main_page.is_filtering_by_price_correct('', price_to), \
                'The filtering is not correct'

    @title("Check filter products by 'price to' (symbols without digits) on main page")
    @pytest.mark.parametrize("price", ('-', ',', '!!', 'abc'))
    def test_filter_products_by_price_to(self, browser, price):
        main_page = BasePage(browser, link)
        main_page.open()
        price_from = '0'
        price_to = price

        main_page.filter_products_by_price(price_from, price_to)

        with step('Check that filtering by price is correct'):
            assert main_page.is_filtering_by_price_correct(price_from, ''), \
                'The filtering is not correct'

    @title("Check copy-paste value (digits with other symbols) in 'price from'")
    @pytest.mark.xfail(reason='Bug is not fixed', run=True)
    @pytest.mark.parametrize("price", ('1 1', '1    1', 'ad44re'))
    def test_copy_paste_price_from_digits(self, browser, price):
        main_page = BasePage(browser, link)
        main_page.open()
        price_from = price
        price_to = '1000'

        main_page.filter_products_by_price_copy_paste(price_from, price_to)

        # remove all non-digit symbols from price
        price_from_after_processing = re.sub(r'\D', '', price_from)

        with step('Check that filtering by price is correct'):
            assert main_page.is_filtering_by_price_correct(price_from_after_processing, price_to), \
                'The filtering is not correct'

    @title("Check copy-paste value (digits with other symbols) in 'price to'")
    @pytest.mark.xfail(reason='Bug is not fixed', run=True)
    @pytest.mark.parametrize("price", ('1 1', '1    1', 'ad4re'))
    def test_copy_paste_price_to_digits(self, browser, price):
        main_page = BasePage(browser, link)
        main_page.open()
        price_from = '0'
        price_to = price

        main_page.filter_products_by_price_copy_paste(price_from, price_to)

        # remove all non-digit symbols from price
        price_to_after_processing = re.sub(r'\D', '', price_to)

        with step('Check that filtering by price is correct'):
            assert main_page.is_filtering_by_price_correct(price_from, price_to_after_processing), \
                'The filtering is not correct'

    @title("Check copy-paste value (symbols without digits) in 'price from'")
    @pytest.mark.parametrize("price", ('---', '!,!', '!!', 'abc'))
    def test_copy_paste_price_from(self, browser, price):
        main_page = BasePage(browser, link)
        main_page.open()
        price_from = price
        price_to = '1000'

        main_page.filter_products_by_price(price_from, price_to)

        with step('Check that filtering by price is correct'):
            assert main_page.is_filtering_by_price_correct('', price_to), \
                'The filtering is not correct'

    @title("Check copy-paste value (symbols without digits) in 'price to'")
    @pytest.mark.parametrize("price", ('---', '!,!', '!!', 'abc'))
    def test_copy_paste_price_to(self, browser, price):
        main_page = BasePage(browser, link)
        main_page.open()
        price_from = '0'
        price_to = price

        main_page.filter_products_by_price(price_from, price_to)

        with step('Check that filtering by price is correct'):
            assert main_page.is_filtering_by_price_correct(price_from, ''), \
                'The filtering is not correct'
