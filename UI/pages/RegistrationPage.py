from .BasePage import BasePage
from .locators import BasePageLocators, RegistrationPageLocators


class RegistrationPage(BasePage):
    # check that sort drop-down is not present on the page
    def is_dropdown_present(self):
        self.is_element_present(*BasePageLocators.SORT_DROPDOWN)
    
    def register_new_user(self, first_name, last_name, email, password):
        first_name_field = self.browser.find_element(*RegistrationPageLocators.FIRST_NAME_FIELD)
        first_name_field.send_keys(first_name)
        last_name_field = self.browser.find_element(*RegistrationPageLocators.LAST_NAME_FIELD)
        last_name_field.send_keys(last_name)
        email_field = self.browser.find_element(*RegistrationPageLocators.EMAIL_FIELD)
        email_field.send_keys(email)
        password_field = self.browser.find_element(*RegistrationPageLocators.PASSWORD_FIELD)
        password_field.send_keys(password)
        register_button = self.browser.find_element(*RegistrationPageLocators.REGISTER_BUTTON)
        register_button.click()    
