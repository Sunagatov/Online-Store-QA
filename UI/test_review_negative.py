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
@pytest.mark.parametrize('review_text', parameterize_text_review_negative)
def test_review_negative(review_text, browser):
    with step('Login user'):
            login_user(browser, link)
    with step('Delete old review'):
        delete_old_review(browser, link)
    with step('Add review and rating'):
        product_page = ProductPage(browser, browser.current_url)
        product_page.click_add_review()
        product_page.set_rating()
        product_page.fill_review(review_text[0])
