from .pages.profile_page import ProfilePage
from .pages.edit_profile_page import EditProfilePage
from .set_of_steps import go_to_edit_profile_page
from .configs import link, new_last_name_positive

from allure import step, title, severity, story
import pytest


@title("Test Change Last Name")
@story("Personal Account")
# @allure.description("")
# @allure.tag("")
@severity(severity_level="MAJOR")
@pytest.mark.parametrize('new_last_name', new_last_name_positive)
def test_user_can_change_last_name(browser, new_last_name):
    with step('Go to Edit Profile Page'):        
        go_to_edit_profile_page(browser, link)
    with step('Enter new Last Name'):
        page = EditProfilePage(browser, browser.current_url)
        page.change_last_name(new_last_name)
    with step('Click "Save Changes" button'):
        page.save_change()
    #  with step('Assert Success massage is present'):
        #  assert page.is_success_message_present('Your Last Name was changed'), 'Success message is not present'
    with step('Assert New Last Name is present in profile'):
        page = ProfilePage(browser, browser.current_url)
        assert page.is_new_last_name_present(new_last_name), 'New Last Name is not present in profile'
