from selenium.webdriver.common.by import By


class BasePageLocators:
    LOGIN_LINK = (By.CSS_SELECTOR, '[href="/auth/login"]')
    PROFILE_LINK = (By.CSS_SELECTOR, '[href="/profile"]')


class LoginPageLocators:
    REGISTER_BUTTON = (By.CSS_SELECTOR, '[href="/auth/registration"]')
    EMAIL_FIELD = (By.ID, 'email')
    PASSWORD_FIELD = (By.ID, 'password')
    LOGIN_BUTTON = (By.CSS_SELECTOR, '[type="submit"]')


class RegistrationPageLocators:
    FIRST_NAME_FIELD = (By.ID, 'firstName')
    LAST_NAME_FIELD = (By.ID, 'lastName')
    EMAIL_FIELD = (By.ID, 'email')
    PASSWORD_FIELD = (By.ID, 'password')
    REGISTER_BUTTON = (By.CSS_SELECTOR, '[type="submit"]')


class ProfilePageLocators:
    EDIT_BUTTON = (By.XPATH, '/html/body/main/div/div/div[3]/div/button')
    EMAIL_FIELD = (By.XPATH, '(//ul/li[4])[1]')
    FIRST_NAME_FIELD = (By.XPATH, '(//ul/li[1])[1]')
    LAST_NAME_FIELD = (By.XPATH, '(//ul/li[2])[1]')


class EditProfilePageLocators:
    EMAIL_FIELD = (By.ID, 'email')
    FIRST_NAME_FIELD = (By.ID, 'firstName')
    LAST_NAME_FIELD = (By.ID, 'lastName')
    SAVE_CHANGE_BUTTON = (By.CSS_SELECTOR, '[type="submit"]')
    #  SUCCESS_MESSAGE = (By.ID, 'success')
