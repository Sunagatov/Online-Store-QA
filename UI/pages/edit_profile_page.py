from .base_page import BasePage
from .locators import EditProfilePageLocators


class EditProfilePage(BasePage):
    def change_email(self, new_email):
        email_field = self.browser.find_element(*EditProfilePageLocators.EMAIL_FIELD)
        email_field.clear()
        email_field.send_keys(new_email)

    def change_first_name(self, new_first_name):
        first_name_field = self.browser.find_element(*EditProfilePageLocators.FIRST_NAME_FIELD)
        first_name_field.clear()
        first_name_field.send_keys(new_first_name)

    def change_last_name(self, new_last_name):
        last_name_field = self.browser.find_element(*EditProfilePageLocators.LAST_NAME_FIELD)
        last_name_field.clear()
        last_name_field.send_keys(new_last_name)

    def save_change(self):
        save_change_button = self.browser.find_element(*EditProfilePageLocators.SAVE_CHANGE_BUTTON)
        save_change_button.click()

    def go_to_main_page(self):
        main_page_link = self.browser.find_element(*EditProfilePageLocators.MAIN_PAGE_LINK)
        main_page_link.click()
    
    def is_error_message_first_name_present(self, error_message):
        try:
            message_empty = self.browser.find_element(*EditProfilePageLocators.EMPTY_FIRST_NAME_MESSAGE).text
        except:
            message_empty = ''
        try:
            message_nonlatin = self.browser.find_element(*EditProfilePageLocators.NONLATIN_FIRST_NAME_MESSAGE).text
        except:
            message_nonlatin = ''
        try:
            message_server_error = self.browser.find_element(*EditProfilePageLocators.SERVER_ERROR_MESSAGE).text
        except:
            message_server_error = ''        
        if (message_empty in error_message) or \
           (message_nonlatin in error_message) or \
           (message_server_error in error_message):
            return True
        else:
            return False
    
    def is_error_message_last_name_present(self, error_message):
        try:
            message_empty = self.browser.find_element(*EditProfilePageLocators.EMPTY_LAST_NAME_MESSAGE).text
        except:
            message_empty = ''
        try:
            message_nonlatin = self.browser.find_element(*EditProfilePageLocators.NONLATIN_LAST_NAME_MESSAGE).text
        except:
            message_nonlatin = ''
        try:
            message_server_error = self.browser.find_element(*EditProfilePageLocators.SERVER_ERROR_MESSAGE).text
        except:
            message_server_error = ''        
        if (message_empty in error_message) or \
           (message_nonlatin in error_message) or \
           (message_server_error in error_message):
            return True
        else:
            return False

'''    def is_success_message_present(self, success_message):
        message_element = self.browser.find_element(*EditProfilePageLocators.SUCCESS_MESSAGE)
        if message_element.text == success_message:
            return True
        else:
            return False
'''
