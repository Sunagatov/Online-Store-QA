from .pages.BasePage import BasePage
from .pages.ProfilePage import ProfilePage
from .pages.EditProfilePage import EditProfilePage
from .set_of_steps import go_to_edit_profile_page
from .configs import link, new_first_name_negative

from allure import step, title, severity, story, severity_level
import pytest


@title("Test Change First Name Negative")
@story("Personal Account")
# @allure.description("")
# @allure.tag("")
@severity(severity_level.NORMAL)
@pytest.mark.parametrize('new_first_name', new_first_name_negative)
def test_user_cant_change_first_name(browser, new_first_name):
    with step('Go to Edit Profile Page'):        
        go_to_edit_profile_page(browser, link)
    with step('Enter new Negative First Name'):
        page = EditProfilePage(browser, browser.current_url)
        page.change_first_name(new_first_name)
    with step('Click "Save Changes" button'):
        page.save_change()    
    with step('Assert Error Message is Present'):                
        assert page.is_error_message_first_name_present(('Invalid name format. Use extended Latin letters, spaces, and specified symbols', 
                                              'name is required', 
                                              'Server Error: Internal server error')
                                             ), 'Error message is not present'
    with step('Go to Main Page'):        
        page.go_to_main_page()
    with step('Go to Profile Page'):
        page = BasePage(browser, browser.current_url)
        page.go_to_profile_page()        
    with step('Assert New Negative First Name is not Present in Profile'):
        page = ProfilePage(browser, browser.current_url)
        assert not page.is_new_first_name_present(new_first_name), 'New Negative First Name is Present in Profile'
        