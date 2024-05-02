from selenium.webdriver.common.by import By


class BasePageLocators:
    ADD_TO_CART_BUTTON = (By.XPATH, '//li[2]/div/div[2]/div/button')
    ADD_TO_CART_BUTTON_2 = (By.XPATH, '//li[3]/div/div[2]/div/button')
    CART_LINK = (By.CSS_SELECTOR, '[href="/cart"]')
    CART_ICON = (By.XPATH, '//header/div/a[3]/button/div[2]/span')  # same on every pages
    LOGIN_LINK = (By.CSS_SELECTOR, '[href="/auth/login"]')
    PRODUCT_NAME = (By.XPATH, '//li[2]/div/a/div[2]/h2')
    PRODUCT_PRICE = (By.XPATH, '//li[2]/div/div[2]/p')
    PRODUCT_WEIGHT = (By.XPATH, '//li[2]//div[1]//a[1]//div[2]//div[1]//span[2]')
    PROFILE_LINK = (By.CSS_SELECTOR, '[href="/profile"]')
    SORT_DROPDOWN = (By.XPATH, "//*[contains(text(), 'Sort by:')]")


class CartPageLocators:
    AMOUNT = (By.XPATH, '/html/body/main/div/div[1]/div[1]/div[2]/div/div[1]/span')
    REMOVE_BUTTON = (By.ID, 'remove-all-btn')
    CONTINUE_SHOPPING_BUTTON = (By.CSS_SELECTOR, 'button[type="button"]')
    EMPTY_CART_MESSAGE = (By.XPATH, "//*[contains(text(), 'Your cart is empty')]")    
    MINUS_BUTTON = (By.XPATH, '(//button[@id="min-btn"])[1]')
    MINUS_2_BUTTON = (By.XPATH, '(//button[@id="min-btn"])[2]')
    PLUS_BUTTON = (By.XPATH, '(//button[@id="plus-btn"])[1]')
    PLUS_2_BUTTON = (By.XPATH, '(//button[@id="plus-btn"])[2]')
    PRODUCT_NAME = (By.XPATH, '//div/div[1]/div/div[2]/p[1]')
    PRODUCT_COST = (By.XPATH, '//div/div[1]/div[1]/div[2]/p[3]')
    PRODUCT_WEIGHT = (By.XPATH, "//p[@class='font-medium text-placeholder']")
    PRODUCT_2_COST = (By.XPATH, '//div/div[1]/div[2]/div[2]/p[3]')
    SUBTOTAL = (By.XPATH, '/html/body/main/div/div[2]/p[2]')


class EditProfilePageLocators:
    EMAIL_FIELD = (By.ID, 'email')
    FIRST_NAME_FIELD = (By.ID, 'firstName')
    LAST_NAME_FIELD = (By.ID, 'lastName')
    SAVE_CHANGE_BUTTON = (By.CSS_SELECTOR, '[type="submit"]')
    MAIN_PAGE_LINK = (By.CSS_SELECTOR, '[href="/"]')
    #  SUCCESS_MESSAGE = (By.ID, 'success')
    EMPTY_FIRST_NAME_MESSAGE = (By.XPATH, "//*[contains(text(), 'name is required')]")
    NONLATIN_FIRST_NAME_MESSAGE = (By.XPATH, "//*[contains(text(), 'Invalid name format. Use extended Latin letters, spaces, and specified symbols')]")
    SERVER_ERROR_MESSAGE = (By.XPATH, "//*[contains(text(), 'Server Error: Internal server error')]")
    EMPTY_LAST_NAME_MESSAGE = (By.XPATH, "//*[contains(text(), 'Last name is required')]")
    NONLATIN_LAST_NAME_MESSAGE = (By.XPATH, "//*[contains(text(), 'Invalid Last name format. Use extended Latin letters')]")    
    #  SERVER_ERROR_MESSAGE = (By.XPATH, '/html/body/main/div/div/div[3]/form/div[9]/div')    
    #  EMPTY_NONLATIN_MESSAGE = (By.CSS_SELECTOR, '.mt-2.font-medium.text-negative')
    #  SERVER_ERROR_MESSAGE = (By.CSS_SELECTOR, '.mt-4.text-negative')    


class LoginPageLocators:    
    REGISTER_BUTTON = (By.XPATH, '/html/body/main/div/div[2]/div[2]/a[2]/button')
    # REGISTER_BUTTON = (By.XPATH, '//button[@type="button" and text()="Register"]')
    EMAIL_FIELD = (By.ID, 'email')
    PASSWORD_FIELD = (By.ID, 'password')
    LOGIN_BUTTON = (By.CSS_SELECTOR, '[type="submit"]')


class ProfilePageLocators:
    EDIT_BUTTON = (By.XPATH, '//button[@type="button"]/span[contains(text(), "Edit")]')
    # EDIT_BUTTON = (By.XPATH, '/html/body/main/div/div/div[3]/div/button')
    EMAIL_FIELD = (By.XPATH, '(//ul/li[4])[1]')
    FIRST_NAME_FIELD = (By.XPATH, '(//ul/li[1])[1]')
    LAST_NAME_FIELD = (By.XPATH, '(//ul/li[2])[1]')


class RegistrationPageLocators:
    FIRST_NAME_FIELD = (By.ID, 'firstName')
    LAST_NAME_FIELD = (By.ID, 'lastName')
    EMAIL_FIELD = (By.ID, 'email')
    PASSWORD_FIELD = (By.ID, 'password')
    REGISTER_BUTTON = (By.CSS_SELECTOR, '[type="submit"]')
