from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException

from .base_page import BasePage
from .locators import BasePageLocators, LoginPageLocators


class LoginPage(BasePage):
    def go_to_registration_page(self):
        link = self.browser.find_element(*LoginPageLocators.REGISTER_BUTTON)
        link.click()
    
    # check that sort drop-down is not present on the page    
    def is_dropdown_present(self):
        self.is_element_present(*BasePageLocators.SORT_DROPDOWN)

    def is_login_page(self):
        is_true = True
        try:
            WebDriverWait(self.browser, 4).until(
                ec.text_to_be_present_in_element(LoginPageLocators.WELCOME_BACK, 'Welcome back')
            )            
        except TimeoutException:
            is_true = False
        return is_true

    def login_existing_user(self, email, password):
        email_field = self.browser.find_element(*LoginPageLocators.EMAIL_FIELD)
        password_field = self.browser.find_element(*LoginPageLocators.PASSWORD_FIELD)
        login_button = self.browser.find_element(*LoginPageLocators.LOGIN_BUTTON)
        email_field.send_keys(email)
        password_field.send_keys(password)
        login_button.click()    
    