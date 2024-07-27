from allure import step, title, severity, story, severity_level
from time import sleep

from .pages.base_page import BasePage
from .pages.favorites_page import FavoritesPage
from .pages.product_page import ProductPage
from .pages.cart_page import CartPage
from .set_of_steps import login_user, remove_products_from_cart_and_favorites
from .configs import link


@story("Product Page")
# @allure.description("")
# @allure.tag("")
@severity(severity_level.CRITICAL)
class TestProductPage:

    # ----------- GUEST ------------

    @title("Test main page product data is equal product page. User is not logged-in")
    # @pytest.mark.skip()
    def test_product_data_guest(self, browser):
        with step('Open main page'):            
            page = BasePage(browser, link)
            page.open()
            sleep(2)  # waiting is mandatory (do not remove)
        with step('Get product data from main page'):
            main_page_product_name = page.get_product_name()
            main_page_product_price = page.get_product_price()
            main_page_product_weight = page.get_product_weight()
            main_page_product_rating = page.get_product_rating()
            main_page_product_reviews = page.get_product_reviews()
        with step('Go to product page'):
            page.go_to_product_page()
            sleep(2)  # waiting is mandatory (do not remove)
            page = ProductPage(browser, browser.current_url)
        with step('Check product name'):            
            product_page_product_name = page.get_product_name()
            assert product_page_product_name == main_page_product_name, \
                'Product names is not equal on main and product pages'
        with step('Check product price'):
            product_page_product_price = page.get_product_price()
            assert product_page_product_price == main_page_product_price, \
                'Product price is not equal on main and product pages'
        with step('Check product weight'):
            product_page_product_weight = page.get_product_weight()
            assert product_page_product_weight == main_page_product_weight, \
                'Product weight is not equal on main and product pages'
        with step('Check product rating'):
            product_page_product_rating = page.get_product_rating()
            assert product_page_product_rating == main_page_product_rating, \
                'Product rating is not equal on main and product pages'
        with step('Check product reviews count'):
            product_page_product_reviews = page.get_product_reviews()
            assert product_page_product_reviews == main_page_product_reviews, \
                'Product reviews count is not equal on main and product pages'

    @title('Test header links. User is not logged-in')
    # @pytest.mark.skip()
    def test_header_links_guest(self, browser):
        with step('Open main page'):            
            page = BasePage(browser, link)
            page.open()
            sleep(2)  # waiting is mandatory (do not remove)
        with step('Go to product page'):
            page.go_to_product_page()
            sleep(2)  # waiting is mandatory (do not remove)
            page = ProductPage(browser, browser.current_url)
        with step('Assert main page link is presented and clickable'):
            assert page.is_main_page_link_present(), 'Main page link is not presented'
            assert page.is_main_page_link_clickable(), 'Main page link is not clickable'
        with step('Assert favorites page link is presented and clickable'):
            assert page.is_favorites_page_link_present(), 'Favorites page link is not presented'
            assert page.is_favorites_page_link_clickable(), 'Favorites page link is not clickable'
        with step('Assert login page link is presented and clickable'):
            assert page.is_login_page_link_present(), 'Login page link is not presented'
            assert page.is_login_page_link_clickable(), 'Login page link is not clickable'
        with step('Assert shopping cart page link is presented and clickable'):
            assert page.is_cart_page_link_present(), 'Cart page link is not presented'
            assert page.is_cart_page_link_clickable(), 'Cart page link is not clickable'
    
    @title('Add product to cart and change quantity. User is not logged-in')
    # @pytest.mark.skip()
    def test_add_to_cart_guest(self, browser):
        with step('Open main page'):            
            page = BasePage(browser, link)
            page.open()
            sleep(2)  # waiting is mandatory (do not remove)
        with step('Go to product page'):
            page.go_to_product_page()
            sleep(2)  # waiting is mandatory (do not remove)
            page = ProductPage(browser, browser.current_url)
            product_page_product_name = page.get_product_name()
        with step('Add product to cart'):
            page.add_product_to_cart()
            assert page.is_change_cart_counter('1'), 'Cart counter is not change'
        with step('Click on Plus Button'):            
            page.click_plus_button()
            sleep(2)  # waiting is mandatory (do not remove)
            assert page.is_change_cart_counter('2'), 'Cart counter is not change'
            assert page.is_change_amount('2'), 'Amount is not change'
        with step('Click on Minus Button'):
            page.click_minus_button()
            sleep(2)  # waiting is mandatory (do not remove)
            assert page.is_change_cart_counter('1'), 'Cart counter is not change'
            assert page.is_change_amount('1'), 'Amount is not change'
        with step('Check product in the cart'):
            page.go_to_cart_page()
            page = CartPage(browser, browser.current_url)
            assert page.is_product_in_cart(product_page_product_name), 'There is not product in the cart'

    @title('Add product to favorites. User is not logged-in')
    # @pytest.mark.skip()
    def test_add_to_favorites_guest(self, browser):
        with step('Open main page'):            
            page = BasePage(browser, link)
            page.open()
            sleep(2)  # waiting is mandatory (do not remove)
        with step('Go to product page'):
            page.go_to_product_page()
            sleep(2)  # waiting is mandatory (do not remove)
            page = ProductPage(browser, browser.current_url)
            product_page_product_name = page.get_product_name()
        with step('Add product to favorires'):
            page.add_product_to_favorites()            
            assert page.is_heart_red(), 'Heart button is not red'
            assert page.is_change_favorites_counter('1'), \
                'Header favorites counter does not changes'
        with step('Check product in the favorites list'):
            page.go_to_favorites_page()            
            page = FavoritesPage(browser, browser.current_url)
            assert page.is_product_in_favorites(product_page_product_name), \
                'There is not product in favorites list'
        with step('Return to product page'):
            page.go_to_product_page()            
            sleep(2)  # waiting is mandatory (do not remove)
            page = ProductPage(browser, browser.current_url)
        with step('Remove product from favorites'):
            page.remove_product_from_favorites()            
            assert page.is_heart_transparent(), 'Heart button is not transparent'
            assert page.is_favorites_page_icon_has_not_counter(), 'Header favorites counter has not disappeared'            

    # ----------- USER ------------

    @title("Test main page product data is equal product page. User is logged-in")
    # @pytest.mark.skip()
    def test_product_data_user(self, browser):
        with step('Login User'):            
            login_user(browser, link)
            sleep(2)  # waiting is mandatory (do not remove)
        with step('Remove products from cart and favorites'):
            remove_products_from_cart_and_favorites(browser, link)        
        with step('Get product data from main page'):
            page = BasePage(browser, link)
            main_page_product_name = page.get_product_name()
            main_page_product_price = page.get_product_price()
            main_page_product_weight = page.get_product_weight()
            main_page_product_rating = page.get_product_rating()
            main_page_product_reviews = page.get_product_reviews()
        with step('Go to product page'):
            page.go_to_product_page()
            sleep(2)  # waiting is mandatory (do not remove)
            page = ProductPage(browser, browser.current_url)
        with step('Check product name'):            
            product_page_product_name = page.get_product_name()
            assert product_page_product_name == main_page_product_name, \
                'Product names is not equal on main and product pages'
        with step('Check product price'):
            product_page_product_price = page.get_product_price()
            assert product_page_product_price == main_page_product_price, \
                'Product price is not equal on main and product pages'
        with step('Check product weight'):
            product_page_product_weight = page.get_product_weight()
            assert product_page_product_weight == main_page_product_weight, \
                'Product weight is not equal on main and product pages'
        with step('Check product rating'):
            product_page_product_rating = page.get_product_rating()
            assert product_page_product_rating == main_page_product_rating, \
                'Product rating is not equal on main and product pages'
        with step('Check product reviews count'):
            product_page_product_reviews = page.get_product_reviews()
            assert product_page_product_reviews == main_page_product_reviews, \
                'Product reviews count is not equal on main and product pages'

    @title('Test header links. User is logged-in')
    # @pytest.mark.skip()
    def test_header_links_user(self, browser):
        with step('Login User'):            
            login_user(browser, link)
            sleep(2)  # waiting is mandatory (do not remove)
        with step('Go to product page'):
            page = BasePage(browser, link)
            page.go_to_product_page()
            sleep(2)  # waiting is mandatory (do not remove)
            page = ProductPage(browser, browser.current_url)
        with step('Assert main page link is presented and clickable'):
            assert page.is_main_page_link_present(), 'Main page link is not presented'
            assert page.is_main_page_link_clickable(), 'Main page link is not clickable'
        with step('Assert favorites page link is presented and clickable'):
            assert page.is_favorites_page_link_present(), 'Favorites page link is not presented'
            assert page.is_favorites_page_link_clickable(), 'Favorites page link is not clickable'
        with step('Assert profile page link is presented and clickable'):
            assert page.is_profile_page_link_present(), 'Profile page link is not presented'
            assert page.is_profile_page_link_clickable(), 'Profile page link is not clickable'
        with step('Assert shopping cart page link is presented and clickable'):
            assert page.is_cart_page_link_present(), 'Cart page link is not presented'
            assert page.is_cart_page_link_clickable(), 'Cart page link is not clickable'

    @title('Add product to cart and change quantity. User is logged-in')
    # @pytest.mark.skip()
    def test_add_to_cart_user(self, browser):    
        with step('Login user'):            
            login_user(browser, link)            
        with step('Remove products from cart and favorites'):
            remove_products_from_cart_and_favorites(browser, link)
        with step('Go to product page'):
            page = BasePage(browser, link)
            page.go_to_product_page()
            sleep(2)  # waiting is mandatory (do not remove)
            page = ProductPage(browser, browser.current_url)
            product_page_product_name = page.get_product_name()
        with step('Add product to cart'):
            page.add_product_to_cart()
            assert page.is_change_cart_counter('1'), 'Cart counter is not change'
        with step('Click on Plus Button'):            
            page.click_plus_button()
            sleep(2)  # waiting is mandatory (do not remove)
            assert page.is_change_cart_counter('2'), 'Cart counter is not change'
            assert page.is_change_amount('2'), 'Amount is not change'
        with step('Click on Minus Button'):
            page.click_minus_button()
            sleep(2)  # waiting is mandatory (do not remove)
            assert page.is_change_cart_counter('1'), 'Cart counter is not change'
            assert page.is_change_amount('1'), 'Amount is not change'
        with step('Check product in the cart'):
            page.go_to_cart_page()
            page = CartPage(browser, browser.current_url)
            assert page.is_product_in_cart(product_page_product_name), 'There is not product in the cart'
    
    @title('Add product to favorires. User is logged-in')
    # @pytest.mark.skip()
    def test_add_to_favorites_user(self, browser):
        with step('Login user'):            
            login_user(browser, link)
        with step('Go to product page'):
            page = BasePage(browser, link)
            page.go_to_product_page()
            sleep(2)  # waiting is mandatory (do not remove)
            page = ProductPage(browser, browser.current_url)
            product_page_product_name = page.get_product_name()
        with step('Add product to favorires'):
            page.add_product_to_favorites()            
            assert page.is_heart_red(), 'Heart button is not red'
            assert page.is_change_favorites_counter('1'), \
                'Header favorites counter does not changes'
        with step('Check product in the favorites list'):
            page.go_to_favorites_page()            
            page = FavoritesPage(browser, browser.current_url)
            assert page.is_product_in_favorites(product_page_product_name), \
                'There is not product in favorites list'
        with step('Return to product page'):
            page.go_to_product_page()            
            sleep(2)  # waiting is mandatory (do not remove)
            page = ProductPage(browser, browser.current_url)
        with step('Remove product from favorites'):
            page.remove_product_from_favorites()            
            assert page.is_heart_transparent(), 'Heart button is not transparent'
            assert page.is_favorites_page_icon_has_not_counter(), 'Header favorites counter has not disappeared'            
