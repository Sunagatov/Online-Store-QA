from allure import step, title, severity, story, severity_level
from time import sleep
import pytest

from .pages.base_page import BasePage
from .pages.product_page import ProductPage
from .pages.login_page import LoginPage
from .pages.profile_page import ProfilePage
from .set_of_steps import login_user, delete_old_review
from .configs import link, first_name
from data.text_review import parameterize_text_review_negative


@story("Review, Rating")
# @allure.description("")
# @allure.tag("")
@severity(severity_level.NORMAL)
class TestReviewNegative:
    @pytest.mark.xfail(reason="Requirements is not approved", run=True)
    def test_non_latin_review(self, browser):
        with step('Login user'):
                login_user(browser, link)
        with step('Delete old review'):
            delete_old_review(browser, link)
        with step('Add non latin letters review'):
            product_page = ProductPage(browser, browser.current_url)
            product_page.click_add_review()
            product_page.set_rating()
            product_page.fill_review(parameterize_text_review_negative[0][0])
            assert product_page.is_submit_button_not_active(), "Submit review button is active"

    @pytest.mark.xfail(reason="Requirements is not approved", run=True)
    def test_not_allowed_symbols_review(self, browser):
        with step('Login user'):
                login_user(browser, link)
        with step('Delete old review'):
            delete_old_review(browser, link)
        with step('Add not allowed symbols review'):
            product_page = ProductPage(browser, browser.current_url)
            product_page.click_add_review()
            product_page.set_rating()
            product_page.fill_review(parameterize_text_review_negative[1][0])
            assert product_page.is_submit_button_not_active(), "Submit review button is active"

    def test_empty_review(self, browser):
        with step('Login user'):
                login_user(browser, link)
        with step('Delete old review'):
            delete_old_review(browser, link)
        with step('Add empty review'):
            product_page = ProductPage(browser, browser.current_url)
            product_page.click_add_review()
            product_page.set_rating()
            product_page.fill_review(parameterize_text_review_negative[2][0])
            assert product_page.is_submit_button_not_active(), "Submit review button is active"

    def test_1501_char_review(self, browser):
        with step('Login user'):
                login_user(browser, link)
        with step('Delete old review'):
            delete_old_review(browser, link)
        with step('Add 1501 char review'):
            product_page = ProductPage(browser, browser.current_url)
            product_page.click_add_review()
            product_page.set_rating()
            product_page.fill_review(parameterize_text_review_negative[3][0])
            counter = product_page.get_review_symbols_counter()
            assert counter == 1500, "User can add 1501 symbols review"
