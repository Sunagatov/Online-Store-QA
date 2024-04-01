from .pages.base_page import BasePage
from .pages.login_page import LoginPage
from .pages.profile_page import ProfilePage
from .pages.edit_profile_page import EditProfilePage
from .configs import link, email, password, new_first_name


from time import sleep
from allure import step, title, severity, story
import pytest


@title("Test Change First Name")
@story("Personal Account")
# @allure.description("")
# @allure.tag("")
@severity(severity_level="MAJOR")
def test_user_can_change_first_name(browser):
    with step('Open main page'):
        page = BasePage(browser, link)
        page.open()
    with step('Go to login page'):
        page.go_to_login_page()
    with step('Login existing user'):
        login_page = LoginPage(browser, browser.current_url)
        login_page.login_existing_user(email, password)
    with step('Go to profile page'):
        page = BasePage(browser, browser.current_url)
        page.go_to_profile_page()
    with step('Click "Edit" button'):
        page = ProfilePage(browser, browser.current_url)
        page.go_to_edit_page()
    with step('Enter new First Name'):
        page = EditProfilePage(browser, browser.current_url)
        page.change_first_name(new_first_name)
    with step('Click "Save Changes" button'):
        page.save_change()
    #  with step('Assert Success massage is present'):
        #  assert page.is_success_message_present('Your First Name was changed'), 'Success message is not present'
    with step('Assert New First Name is present in profile'):
        page = ProfilePage(browser, browser.current_url)
        assert page.is_new_first_name_present(new_first_name), 'New First Name is not present in profile'


sleep(5)
