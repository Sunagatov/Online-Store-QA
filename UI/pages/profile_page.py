from .base_page import BasePage
from .locators import ProfilePageLocators


class ProfilePage(BasePage):
    def go_to_edit_page(self):
        button = self.browser.find_element(*ProfilePageLocators.EDIT_BUTTON)
        button.click()

    def is_new_first_name_present(self, new_first_name):
        first_name_field = self.browser.find_element(*ProfilePageLocators.FIRST_NAME_FIELD)
        if first_name_field.text == f'First name:\n{new_first_name}':
            return True
        else:
            return False
