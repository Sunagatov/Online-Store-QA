from allure import step, title, severity, story, severity_level
# import pytest

from .pages.base_page import BasePage
from .configs import link


@story("Product Catalog")
@title("Test for Main Page")
# @allure.description("")
# @allure.tag("")
@severity(severity_level.CRITICAL)
class TestMainPage:
    def test_sort_product_by_high_rating(self, browser):
        main_page = BasePage(browser, link)
        main_page.open()
        main_page.sort_by('rating', 'high')

        with step('Check that the sorting is correct'):
            assert main_page.is_sorting_correct('rating', 'high'), 'The sorting is not correct'
