from allure import step, title, severity, story, severity_level
import pytest
# from time import sleep

from .pages.BasePage import BasePage
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
    @pytest.mark.xfail(reason='Bug is not fixed', run=True)
    def test_filter_products_by_price(self, browser):
        main_page = BasePage(browser, link)
        main_page.open()
        price_from = '4'
        price_to = '5.5'
        main_page.filter_products_by_price(price_from, price_to)

        with step('Check that filtering by price is correct'):
            assert main_page.is_filtering_by_price_correct(price_from, price_to), 'The filtering is not correct'

    @title("Check filter products by rating on main page")
    def test_filter_products_by_rating(self, browser):
        main_page = BasePage(browser, link)
        main_page.open()

        rating_list = ['4', '3', '2', '1', 'any']
        for rating in rating_list:
            main_page.filter_products_by_rating(rating)
            with step('Check that filtering by rating is correct'):
                assert main_page.is_filtering_by_rating_correct(rating), 'The filtering is not correct'

    @title("Test show more/less button in brand filter")
    def test_brand_show_more_less_button(self, browser):
        main_page = BasePage(browser, link)
        main_page.open()

        brand_list_length_before = main_page.get_brand_list_length()
        main_page.show_more_less_brand()
        brand_list_length_after = main_page.get_brand_list_length()

        with step('Check brand list after click show more button'):
            assert brand_list_length_after > brand_list_length_before, 'The show more brand button does not work'

        main_page.show_more_less_brand()
        brand_list_length_after = main_page.get_brand_list_length()

        with step('Check brand list after click show less button'):
            assert brand_list_length_after == brand_list_length_before, 'The show less brand button does not work'

    @title("Test show more/less button in seller filter")
    def test_seller_show_more_less_button(self, browser):
        main_page = BasePage(browser, link)
        main_page.open()

        seller_list_length_before = main_page.get_seller_list_length()
        main_page.show_more_less_seller()
        seller_list_length_after = main_page.get_seller_list_length()

        with step('Check seller list after click show more button'):
            assert seller_list_length_after > seller_list_length_before, 'The show more seller button does not work'

        main_page.show_more_less_seller()
        seller_list_length_after = main_page.get_seller_list_length()

        with step('Check seller list after click show less button'):
            assert seller_list_length_after == seller_list_length_before, 'The show less seller button does not work'

    @title("Check filter products by brand on main page")
    def test_filter_products_by_brand(self, browser):
        brand = 'Illy'

        main_page = BasePage(browser, link)
        main_page.open()

        products_list_length_before = main_page.get_products_list_length()
        main_page.filter_products_by_brand(brand)

        with step('Check that filtering by brand is correct'):
            assert main_page.is_filtering_by_brand_correct(brand), 'The filtering is not correct'

        # uncheck brand checkbox
        main_page.filter_products_by_brand(brand)
        products_list_length_after = main_page.get_products_list_length()

        with step('Check that all of products is presented'):
            assert products_list_length_before == products_list_length_after, 'All of products is not presented'

    @title("Check reset button on brand filter")
    def test_reset_filter_by_brand(self, browser):
        brand = 'Illy'

        main_page = BasePage(browser, link)
        main_page.open()

        products_list_length_before = main_page.get_products_list_length()
        main_page.filter_products_by_brand(brand)
        main_page.reset_brand_filter()
        products_list_length_after = main_page.get_products_list_length()

        with step('Check that all of products is presented'):
            assert products_list_length_before == products_list_length_after, 'All of products is not presented'

    @title("Check filter products by seller on main page")
    def test_filter_products_by_seller(self, browser):
        seller = 'FreshCup'

        main_page = BasePage(browser, link)
        main_page.open()

        products_list_length_before = main_page.get_products_list_length()
        main_page.filter_products_by_seller(seller)

        with step('Check that filtering by seller is correct'):
            assert main_page.is_filtering_by_seller_correct(seller), 'The filtering is not correct'

        # uncheck seller checkbox
        main_page.filter_products_by_seller(seller)
        products_list_length_after = main_page.get_products_list_length()

        with step('Check that all of products is presented'):
            assert products_list_length_before == products_list_length_after, 'All of products is not presented'

    @title("Check reset button on seller filter")
    def test_reset_filter_by_seller(self, browser):
        seller = 'FreshCup'

        main_page = BasePage(browser, link)
        main_page.open()

        products_list_length_before = main_page.get_products_list_length()
        main_page.filter_products_by_seller(seller)
        main_page.reset_seller_filter()
        products_list_length_after = main_page.get_products_list_length()

        with step('Check that all of products is presented'):
            assert products_list_length_before == products_list_length_after, 'All of products is not presented'

    @title("Test filter badges on product catalog")
    def test_badges(self, browser):
        brand = 'Dunkin-Donuts'
        seller = 'BrewedBliss'

        main_page = BasePage(browser, link)
        main_page.open()

        products_list_length_before = main_page.get_products_list_length()
        main_page.filter_products_by_brand(brand)

        with step('Check that brand filter badge is present'):
            main_page.is_badge_present(brand), 'Badge filter by brand is not presented'

        main_page.filter_products_by_seller(seller)

        with step('Check that seller filter badge is present'):
            main_page.is_badge_present(seller), 'Badge filter by seller is not presented'

        main_page.remove_filter(seller)
        main_page.remove_filter(brand)
        products_list_length_after = main_page.get_products_list_length()

        with step('Check that all of products is presented'):
            assert products_list_length_before == products_list_length_after, 'All of products is not presented'

    @title("Test 'By default' filter badge on product catalog")
    def test_by_default_badge(self, browser):
        brand = 'Dunkin-Donuts'
        seller = 'BrewedBliss'

        main_page = BasePage(browser, link)
        main_page.open()

        products_list_length_before = main_page.get_products_list_length()
        main_page.filter_products_by_brand(brand)
        main_page.filter_products_by_seller(seller)
        main_page.by_default()
        products_list_length_after = main_page.get_products_list_length()

        with step('Check that all of products is presented'):
            assert products_list_length_before == products_list_length_after, 'All of products is not presented'

    @title("Test plus and minus buttons on product card")
    def test_plus_minus_buttons(self, browser):
        main_page = BasePage(browser, link)
        main_page.open()

        main_page.add_product_to_cart()
        with step('Check that cart counter in the header has increased'):
            assert main_page.is_change_cart_counter('1'), 'Cart counter is not change'

        main_page.click_plus_button()
        with step('Check that cart counter in the header has increased'):
            assert main_page.is_change_cart_counter('2'), 'Cart counter is not change'
        with step('Check that counter on the product card has increased'):
            assert main_page.is_change_product_counter('2'), 'Product counter is not change'

        main_page.click_minus_button()
        with step('Check that cart counter in the header has decreased'):
            assert main_page.is_change_cart_counter('1'), 'Cart counter is not change'
        with step('Check that counter on the product card has decreased'):
            assert main_page.is_change_product_counter('1'), 'Product counter is not change'

        main_page.click_minus_button()
        with step('Check that cart counter in the header is not present'):
            assert not main_page.is_cart_counter_present(), 'Cart counter in the header is present'
        with step('Check that add to cart button is present'):
            assert main_page.is_add_to_cart_button_present(), 'Add to cart button is not present'

    @title("Check scroll button")
    def test_scroll_button(self, browser):
        main_page = BasePage(browser, link)
        main_page.open()

        main_page.click_show_more_button()
        main_page.scroll_down()
        main_page.click_scroll_button()

        with step('Check the banner is displayed on the page (after scroll up)'):
            assert main_page.is_banner_displayed(), 'Banner is not displayed'

    @title("Check that 'sort by' dropdown and filter badges is displayed after scroll down")
    def test_dropdown_and_badges_is_displayed_after_scrolling(self, browser):
        brand = 'Dunkin-Donuts'
        seller = 'BrewedBliss'

        main_page = BasePage(browser, link)
        main_page.open()

        main_page.filter_products_by_brand(brand)
        main_page.filter_products_by_seller(seller)

        main_page.scroll_down()

        with step('Check that "sort by" dropdown is displayed'):
            assert main_page.is_sort_dropdown_displayed(), '"Sort by" dropdown is not displayed'
        with step('Check that filter badges is displayed'):
            assert main_page.is_badge_displayed(brand) and main_page.is_badge_displayed(seller),\
                'Filter badges are not displayed'
