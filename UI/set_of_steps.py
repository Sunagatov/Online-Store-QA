from allure import step
from time import sleep
from selenium.webdriver.remote.webdriver import WebDriver

from .pages.base_page import BasePage
from .pages.cart_page import CartPage
from .pages.favorites_page import FavoritesPage
from .pages.login_page import LoginPage
from .pages.profile_page import ProfilePage
from .pages.product_page import ProductPage

from .configs import email, password


def delete_old_review(browser: WebDriver, link: str) -> None:
    with step('Go to product page'):
        main_page = BasePage(browser, link)
        main_page.sort_by('price', 'high')
        main_page.go_to_product_page()
    with step('Delete old review'):
        product_page = ProductPage(browser, browser.current_url)
        product_page.delete_review()


@step('Login User')
def login_user(browser: WebDriver, link: str) -> None:
    with step('Open main page'):
        page = BasePage(browser, link)
        page.open()
    with step('Go to login page'):
        page.go_to_login_page()
    with step('Login existing user'):
        login_page = LoginPage(browser, browser.current_url)
        login_page.login_existing_user(email, password)
        sleep(2)


def go_to_edit_profile_page(browser: WebDriver, link: str) -> None:
    with step('Login existing user'):
        login_user(browser, link)
    with step('Go to profile page'):
        page = BasePage(browser, browser.current_url)
        page.go_to_profile_page()
    with step('Click "Edit" button'):
        page = ProfilePage(browser, browser.current_url)
        page.go_to_edit_page()


@step('Remove products from cart and favorites')
def remove_products_from_cart_and_favorites(browser: WebDriver, link: str) -> None:
    with step('Go to cart page'):
        page = BasePage(browser, link)
        page.go_to_cart_page()        
    with step('Remove all products from the cart'):
        page = CartPage(browser, browser.current_url)
        page.remove_products()        
    with step('Go to favorites page'):
        page.go_to_favorites_page()        
        page = FavoritesPage(browser, browser.current_url)        
    with step('Remove all products from the favorites'):
        page.remove_favorites_products()
        page.go_to_main_page()    
    