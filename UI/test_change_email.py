from .pages.profile_page import ProfilePage
from .pages.edit_profile_page import EditProfilePage
from .set_of_steps import go_to_edit_profile_page
from .configs import link, new_email_positive

from allure import step, title, severity, story
import pytest


@title("Test Change Email")
@story("Personal Account")
# @allure.description("")
# @allure.tag("")
@severity(severity_level="MAJOR")
@pytest.mark.parametrize('new_email', new_email_positive)
def test_user_can_change_email(browser, new_email):
    with step('Go to Edit Profile Page'):        
        go_to_edit_profile_page(browser, link)
    with step('Enter new email'):
        page = EditProfilePage(browser, browser.current_url)
        page.change_email(new_email)
    with step('Click "Save Changes" button'):
        page.save_change()
    #  with step('Assert Success massage is present'):
        #  assert page.is_success_message_present('Your First Name was changed'), 'Success message is not present'
    with step('Assert New Email is present in profile'):
        page = ProfilePage(browser, browser.current_url)
        assert page.is_new_email_present(new_email), 'New Email is not present in profile'
