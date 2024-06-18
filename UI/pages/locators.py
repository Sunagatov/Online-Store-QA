from selenium.webdriver.common.by import By


class BasePageLocators:
    ADD_TO_CART_BUTTON = (By.XPATH, '//li[2]/div/div[2]/div/button')
    ADD_TO_CART_BUTTON_2 = (By.XPATH, '//li[3]/div/div[2]/div/button')    
    # PRODUCT_LINK = (By.CSS_SELECTOR, 'ul li:nth-child(2) [href]')
    PRODUCT_LINK = (By.CSS_SELECTOR, 'ul li:nth-child(3) [href]')
    PRODUCT_NAME = (By.XPATH, '//li[2]/div/a/div[2]/h2')
    PRODUCT_PRICE = (By.XPATH, '//li[2]/div/div[2]/p')
    PRODUCT_RATING = (By.XPATH, '//li[2]/div/a/div[2]/div/span/span[1]')
    PRODUCT_REVIEWS = (By.XPATH, '//li[2]/div/a/div[2]/div/span/span[2]')
    PRODUCT_WEIGHT = (By.XPATH, '//li[2]/div/a/div[2]/div/span[2]')    
    SORT_DROPDOWN = (By.XPATH, '//*[contains(text(), "Sort by:")]')
    SORT_PRICE_HIGH = (By.XPATH, '//span[contains(text(),"Price: High to Low")]')
    SORT_PRICE_LOW = (By.XPATH, '//span[contains(text(),"Price: Low to High")]]')
    SORT_RATING_HIGH = (By.XPATH, '//span[contains(text(),"High rating first")]')
    SORT_RATING_LOW = (By.XPATH, '//span[contains(text(),"Low rating first")]')


class CartPageLocators:
    AMOUNT = (By.XPATH, '/html/body/main/div/div[1]/div[1]/div[2]/div/div[1]/span')
    REMOVE_BUTTON = (By.ID, 'remove-all-btn')
    CONTINUE_SHOPPING_BUTTON = (By.ID, 'continue-btn')
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
    #  SUCCESS_MESSAGE = (By.ID, 'success')
    EMPTY_FIRST_NAME_MESSAGE = (By.XPATH, "//*[contains(text(), 'name is required')]")
    NONLATIN_FIRST_NAME_MESSAGE = (By.XPATH,
            "//*[contains(text(), 'Invalid name format. Use extended Latin letters, spaces, and specified symbols')]")
    SERVER_ERROR_MESSAGE = (By.XPATH, "//*[contains(text(), 'Server Error: Internal server error')]")
    EMPTY_LAST_NAME_MESSAGE = (By.XPATH, "//*[contains(text(), 'Last name is required')]")
    NONLATIN_LAST_NAME_MESSAGE = (By.XPATH,
                                  "//*[contains(text(), 'Invalid Last name format. Use extended Latin letters')]")
    #  SERVER_ERROR_MESSAGE = (By.XPATH, '/html/body/main/div/div/div[3]/form/div[9]/div')
    #  EMPTY_NONLATIN_MESSAGE = (By.CSS_SELECTOR, '.mt-2.font-medium.text-negative')
    #  SERVER_ERROR_MESSAGE = (By.CSS_SELECTOR, '.mt-4.text-negative')


class FavoritesPageLocators:
    PRODUCT_NAME = (By.XPATH, '(//*[starts-with(@href,"/product/")]/following-sibling::div/p)[1]')
    PRODUCT_LINK = (By.XPATH, '//*[starts-with(@href,"/product/")]')
    UNLIKE_BUTTONS = (By.XPATH, '//img[@alt="heart liked"]/parent::button')


class HeaderLocators:
    CART_LINK = (By.CSS_SELECTOR, '[href="/cart"]')
    CART_COUNTER = (By.XPATH, '//*[@href="/cart"]/descendant::span')
    FAVORITES_PAGE_LINK = (By.CSS_SELECTOR, '[href="/favourites"]')
    FAVORITES_COUNTER = (By.XPATH, '//*[@href="/favourites"]/descendant::span')
    # HEART_IMAGE = (By.CSS_SELECTOR, '[alt="heart"]')
    LOGIN_LINK = (By.CSS_SELECTOR, '[href="/auth/login"]')
    MAIN_PAGE_LINK = (By.CSS_SELECTOR, '[href="/"]')
    PROFILE_LINK = (By.CSS_SELECTOR, '[href="/profile"]')


class LoginPageLocators:
    EMAIL_FIELD = (By.ID, 'email')
    LOGIN_BUTTON = (By.CSS_SELECTOR, '[type="submit"]')
    PASSWORD_FIELD = (By.ID, 'password')
    REGISTER_BUTTON = (By.XPATH, '/html/body/main/div/div[2]/div[2]/a[2]/button')    
    # REGISTER_BUTTON = (By.XPATH, '//button[@type="button" and text()="Register"]')    
    WELCOME_BACK = (By.XPATH, '//header/div/div/div/div[1]/h2')


class ProductPageLocators:
    ADD_REVIEW_BUTTON = (By.ID, 'add-review-btn')
    AMOUNT = (By.XPATH, '//*[@id="min-btn"]/following-sibling::span')
    ADD_TO_CART_BUTTON = (By.ID, 'add-btn')
    ADD_TO_FAVORITES_BUTTON = (By.XPATH, '//*[@alt="heart unliked"]/ancestor::button')

    def checkbox(self, rating):        
        checkbox = (By.ID, f'checkbox-{rating}')
        return checkbox

    DELETE_REVIEW_BUTTON = (By.ID, 'delete-review-btn')
    LIKE_OWN_BUTTON = (By.CSS_SELECTOR, '#delete-review-btn + div [id^="like-btn"]')
    LIKE_SOMEONE_BUTTON = (By.CSS_SELECTOR, 'li:nth-child(1) [id^="like-btn"]')
    LIKE_OWN_COUNTER = (By.CSS_SELECTOR, '#delete-review-btn + div [id^="like-btn"] span')
    LIKE_SOMEONE_COUNTER = (By.CSS_SELECTOR, 'li:nth-child(1) [id^="like-btn"] span')
    DISLIKE_OWN_BUTTON = (By.CSS_SELECTOR, '#delete-review-btn + div [id^="dislike-btn"]')
    DISLIKE_SOMEONE_BUTTON = (By.CSS_SELECTOR, 'li:nth-child(1) [id^="dislike-btn"]')
    DISLIKE_OWN_COUNTER = (By.CSS_SELECTOR, '#delete-review-btn + div [id^="dislike-btn"] span')
    DISLIKE_SOMEONE_COUNTER = (By.CSS_SELECTOR, 'li:nth-child(1) [id^="dislike-btn"] span')
    REMOVE_FROM_FAVORITES_BUTTON = (By.XPATH, '//*[@alt="heart liked"]/ancestor::button')
    RED_HEART_IMAGE = (By.CSS_SELECTOR, '[alt="heart liked"]')
    MINUS_BUTTON = (By.ID, 'min-btn')
    PLUS_BUTTON = (By.ID, 'plus-btn')    
    PRODUCT_NAME = (By.XPATH, '(//h2)[1]')    
    PRODUCT_RATING = (By.XPATH, '//h2/following-sibling::div/span[1]')
    PRODUCT_REVIEWS = (By.XPATH, '//h2/following-sibling::div/span[2]')
    PRODUCT_WEIGHT = (By.XPATH, '//h2/following-sibling::div/span[3]')
    RATINGS_IN_REVIEWS_LIST = (By.XPATH, '//ul/li/div[2]/div[1]/span')
    REVIEWS_AMOUNT = (By.XPATH, '//section/div[2]/div/div/div[2]/div/div/div[1]/div[2]')
    REVIEW_AUTHOR = (By.XPATH, '//div[@id="reviewsDropdown"]/following-sibling::div/div/span')
    REVIEW_FIELD = (By.ID, 'review-textarea')
    REVIEW_SYMBOLS_COUNTER = (By.XPATH, '//textarea/following-sibling::div')
    STAR_1 = (By.XPATH, '//*[@for="checkbox-1"]/following-sibling::span')
    STAR_2 = (By.XPATH, '//*[@for="checkbox-2"]/following-sibling::span')
    STAR_3 = (By.XPATH, '//*[@for="checkbox-3"]/following-sibling::span')
    STAR_4 = (By.XPATH, '//*[@for="checkbox-4"]/following-sibling::span')
    STAR_5 = (By.XPATH, '//*[@for="checkbox-5"]/following-sibling::span')    
    STAR_BUTTON_2 = (By.XPATH, '(//div[text()="Rating"]/following-sibling::div/div/div)[2]')
    SUBMIT_REVIEW_BUTTON = (By.ID, 'submit-review-btn')
    TRANSPARENT_HEART_IMAGE = (By.CSS_SELECTOR, '[alt="heart unliked"]')


class ProfilePageLocators:
    EDIT_BUTTON = (By.XPATH, '//button[@type="button"]/span[contains(text(), "Edit")]')
    # EDIT_BUTTON = (By.XPATH, '/html/body/main/div/div/div[3]/div/button')
    EMAIL_FIELD = (By.XPATH, '(//ul/li[4])[1]')
    FIRST_NAME_FIELD = (By.XPATH, '(//ul/li[1])[1]')
    LAST_NAME_FIELD = (By.XPATH, '(//ul/li[2])[1]')
    LOG_OUT_BUTTON = (By.ID, 'logout-btn')


class RegistrationPageLocators:
    FIRST_NAME_FIELD = (By.ID, 'firstName')
    LAST_NAME_FIELD = (By.ID, 'lastName')
    EMAIL_FIELD = (By.ID, 'email')
    PASSWORD_FIELD = (By.ID, 'password')
    REGISTER_BUTTON = (By.CSS_SELECTOR, '[type="submit"]')
