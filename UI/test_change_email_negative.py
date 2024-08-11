from .pages.BasePage import BasePage
from .pages.ProfilePage import ProfilePage
from .pages.EditProfilePage import EditProfilePage
from .set_of_steps import go_to_edit_profile_page
from .configs import link, new_email_negative

from allure import step, title, severity, story, severity_level
import pytest
from time import sleep


@title("Test Change Email Negative")
@story("Personal Account")
# @allure.description("")
# @allure.tag("")
@severity(severity_level.NORMAL)
@pytest.mark.parametrize('new_email', new_email_negative)
def test_user_cant_change_email(browser, new_email):
    with step('Go to Edit Profile Page'):        
        go_to_edit_profile_page(browser, link)        
    with step('Enter new Negative Email'):
        page = EditProfilePage(browser, browser.current_url)
        page.change_email(new_email)
    with step('Click "Save Changes" Button'):
        page.save_change()        
    with step('Go to Main Page'):        
        page.go_to_main_page()
        sleep(2) # waiting is mandatory (do not remove)
    with step('Go to Profile Page'):
        page = BasePage(browser, link)        
        page.go_to_profile_page()                
    with step('Assert New Negative Email is not Present in Profile'):
        page = ProfilePage(browser, browser.current_url)
        assert not page.is_new_email_present(new_email), 'New Negative Email is Present in Profile'
        