from .pages.base_page import BasePage
from .pages.login_page import LoginPage
from .pages.registration_page import RegistrationPage
from .configs import link

from allure import step, title, severity, story, severity_level


@title("Test Fixed Bug: Sort Drop-down is present on Login and Registration page")
@story("Registration/Authorization")
# @allure.description("")
# @allure.tag("")
@severity(severity_level.CRITICAL)
def test_dropdawn_not_present(browser):
    with step('Go to Login Page'):
        page = BasePage(browser, link)
        page.open()    
        page.go_to_login_page()
    with step('Assert Sort Drop-down is not present on Login Page'):
        page = LoginPage(browser, browser.current_url)                
        page.open()
        assert not page.is_dropdown_present(), 'Sort drop-down is present on Login Page'        
    with step('Go to Registration Page'):
        page.go_to_registration_page()
    with step('Assert Sort Drop-down is not present on Registration Page'):
        page = RegistrationPage(browser, browser.current_url)        
        assert not page.is_dropdown_present(), 'Sort drop-down is present on Registration Page'        
