from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from .BasePage import BasePage
from .locators import ProfilePageLocators


class ProfilePage(BasePage):
    def go_to_edit_page(self):
        button = self.browser.find_element(*ProfilePageLocators.EDIT_BUTTON)
        button.click()

    def is_new_email_present(self, new_email):
        email_field = WebDriverWait(self.browser, 3).until(
            ec.presence_of_element_located(ProfilePageLocators.EMAIL_FIELD)
            )
        if email_field.text == f'Email:\n{new_email}':
            return True
        else:
            return False           

    def is_new_first_name_present(self, new_first_name):
        first_name_field = self.browser.find_element(*ProfilePageLocators.FIRST_NAME_FIELD)
        if first_name_field.text == f'First name:\n{new_first_name}':
            return True
        else:
            return False

    def is_new_last_name_present(self, new_last_name):
        last_name_field = self.browser.find_element(*ProfilePageLocators.LAST_NAME_FIELD)
        if last_name_field.text == f'Last name:\n{new_last_name}':
            return True
        else:
            return False    

    def log_out(self):
        log_out_button = self.browser.find_element(*ProfilePageLocators.LOG_OUT_BUTTON)
        log_out_button.click()
