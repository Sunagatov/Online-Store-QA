from allure import step, title, severity, story, severity_level
from time import sleep
import pytest

from .pages.BasePage import BasePage
from .pages.ProductPage import ProductPage
from .pages.LoginPage import LoginPage
from .pages.ProfilePage import ProfilePage
from .set_of_steps import login_user, delete_old_review
from .configs import link, first_name
from data.text_review import parameterize_text_review_positive


@story("Review, Rating")
# @allure.description("")
# @allure.tag("")
@severity(severity_level.NORMAL)
class TestReviewRating:    
    def test_add_review_guest(self, browser):
        with step('Open main page'):            
            main_page = BasePage(browser, link)
            main_page.open()
            sleep(2)  # waiting is mandatory (do not remove)
        with step('Go to product page'):
            main_page.go_to_product_page()
            sleep(2)  # waiting is mandatory (do not remove)
            product_page = ProductPage(browser, browser.current_url)
        with step('Click "Add a review" button'):
            product_page.click_add_review()
            login_page = LoginPage(browser, browser.current_url)            
            assert login_page.is_login_page(), 'The guest was not redirected to the login page'     
    
    def test_add_and_delete_review_user(self, browser):
        with step('Login user'):
            login_user(browser, link)
        with step('Delete old review'):
            delete_old_review(browser, link)
        with step('Get actual rating'):
            product_page = ProductPage(browser, browser.current_url)
            old_rating, old_reviews_amount = product_page.get_actual_rating()
        with step('Add review and rating'):
            product_page.click_add_review()
            product_page.set_rating()
            review_text = "It's a very good coffee"
            product_page.fill_review(review_text)
            counter = product_page.get_review_symbols_counter()
            assert counter == len(review_text), 'Counter does not work'
            product_page.submit_review()
            sleep(2)  # waiting is mandatory (do not remove)
            assert product_page.get_review_author() == first_name, \
                f'Review author {first_name} is not present'
            new_rating, new_reviews_amount = product_page.get_actual_rating()
            assert new_rating == round((old_rating * old_reviews_amount + 2) 
                                       / (old_reviews_amount + 1), 1), \
                'New rating is not correct'            
            assert new_reviews_amount == product_page.get_reviews_amount(), \
                'Review amount is not correct'
        with step('Delete review'):
            product_page.delete_review()
            new_rating, new_reviews_amount = product_page.get_actual_rating()
            assert new_rating == old_rating, 'New rating is not correct'
            assert new_reviews_amount == product_page.get_reviews_amount() \
                   and new_reviews_amount == old_reviews_amount, \
                   'Review amount is not correct'
        
    @pytest.mark.parametrize('review_text', parameterize_text_review_positive)    
    def test_add_review_parametrize(self, browser, review_text):
        with step('Login user'):
            login_user(browser, link)
        with step('Delete old review'):
            delete_old_review(browser, link)
        with step('Add review and rating'):
            product_page = ProductPage(browser, browser.current_url)
            product_page.click_add_review()
            product_page.set_rating()            
            product_page.fill_review(review_text[0])
            counter = product_page.get_review_symbols_counter()
            assert counter == len(review_text[0]), 'Counter does not work'
            product_page.submit_review()
            assert product_page.get_review_author() == first_name, \
                f'Review author {first_name} is not present'       
        with step('Delete review'):
            product_page.delete_review()
    
    def test_like_dislike_someones_review(self, browser):
        with step('Login user'):
            login_user(browser, link)
        with step('Sort product by rating'):
            main_page = BasePage(browser, link)
            main_page.sort_by('rating', 'high')
        with step('Go to product page'):
            main_page.go_to_product_page()
        with step('Delete old review'):
            product_page = ProductPage(browser, browser.current_url)
            product_page.delete_review()
        with step('Delete old like or dislike'):
            product_page.like_someone_review()
            product_page.like_someone_review()
            product_page.dislike_someone_review()
            product_page.dislike_someone_review()
        with step('Like someone review'):
            like_counter_before = product_page.get_like_someone_counter()
            product_page.like_someone_review()
            like_counter_after = product_page.get_like_someone_counter()
            assert like_counter_before == like_counter_after - 1, \
                'Like counter does not work'        
        with step('Dislike someone review'):            
            dislike_counter_before = product_page.get_dislike_someone_counter()
            product_page.dislike_someone_review()
            dislike_counter_after = product_page.get_dislike_someone_counter()
            assert dislike_counter_before == dislike_counter_after - 1, \
                'Dislike counter does not work'
            like_counter_after_dislike = product_page.get_like_someone_counter()
            assert like_counter_after_dislike == like_counter_after - 1, \
                'Like counter has not decreased after dislike'
        with step('Delete dislike someone review'):
            product_page.dislike_someone_review()
            dislike_counter_after_delete = product_page.get_dislike_someone_counter()
            assert dislike_counter_after_delete == dislike_counter_after - 1
        with step('Delete like review'):
            like_counter_before = product_page.get_like_someone_counter()
            product_page.like_someone_review()
            product_page.like_someone_review()
            like_counter_after = product_page.get_like_someone_counter()
            assert like_counter_after == like_counter_before
        
    def test_like_dislike_own_review(self, browser):
        with step('Login user'):
            login_user(browser, link)
        with step('Delete old review'):
            delete_old_review(browser, link)
        with step('Add review and rating'):
            product_page = ProductPage(browser, browser.current_url)
            product_page.click_add_review()
            product_page.set_rating()
            review_text = "It's a very good coffee"
            product_page.fill_review(review_text)
            product_page.submit_review()        
        with step('Like own review'):
            like_counter_before = product_page.get_like_own_counter()
            product_page.like_own_review()
            like_counter_after = product_page.get_like_own_counter()
            assert like_counter_before == like_counter_after - 1, \
                'Like counter does not work'        
        with step('Dislike own review'):            
            dislike_counter_before = product_page.get_dislike_own_counter()
            product_page.dislike_own_review()
            dislike_counter_after = product_page.get_dislike_own_counter()
            assert dislike_counter_before == dislike_counter_after - 1, \
                'Dislike counter does not work'
            like_counter_after_dislike = product_page.get_like_own_counter()
            assert like_counter_after_dislike == like_counter_after - 1, \
                'Like counter has not decreased after dislike'
        with step('Delete dislike review'):
            product_page.dislike_own_review()
            dislike_counter_after_delete = product_page.get_dislike_own_counter()
            assert dislike_counter_after_delete == dislike_counter_after - 1
        with step('Delete like review'):
            like_counter_before = product_page.get_like_own_counter()
            product_page.like_own_review()
            product_page.like_own_review()
            like_counter_after = product_page.get_like_own_counter()
            assert like_counter_after == like_counter_before

    def test_rating_filter(self, browser):
        with step('Login user'):
            login_user(browser, link)
        with step('Sort product by rating'):
            main_page = BasePage(browser, link)
            main_page.sort_by('rating', 'high')
        with step('Go to product page'):
            main_page.go_to_product_page()
        with step('Delete old review'):
            product_page = ProductPage(browser, browser.current_url)
            product_page.delete_review()
        with step('Add review and rating'):            
            product_page.click_add_review()
            product_page.set_rating()
            review_text = "It's a very good coffee"
            product_page.fill_review(review_text)
            product_page.submit_review()
            product_url = browser.current_url
        with step('Log out'):
            product_page.go_to_profile_page()
            profile_page = ProfilePage(browser, browser.current_url)
            profile_page.log_out()
        with step('Go to product page'):
            main_page = BasePage(browser, product_url)
            main_page.open()
        with step('Filter 5'):
            product_page = ProductPage(browser, browser.current_url)            
            ratings = ['5']
            for rating in ratings:
                product_page.rating_checkbox(rating)            
            assert product_page.is_only_filtered_ratings(ratings), "Rating filter does not work"
            for rating in ratings:
                product_page.rating_checkbox(rating)            
        with step('Filter 4'):
            product_page = ProductPage(browser, browser.current_url)            
            ratings = ['4']
            for rating in ratings:
                product_page.rating_checkbox(rating)            
            assert product_page.is_only_filtered_ratings(ratings), "Rating filter does not work"
            for rating in ratings:
                product_page.rating_checkbox(rating)            
        with step('Filter 3'):
            product_page = ProductPage(browser, browser.current_url)            
            ratings = ['3']
            for rating in ratings:
                product_page.rating_checkbox(rating)            
            assert product_page.is_only_filtered_ratings(ratings), "Rating filter does not work"
            for rating in ratings:
                product_page.rating_checkbox(rating)            
        with step('Filter 2'):
            product_page = ProductPage(browser, browser.current_url)            
            ratings = ['2']
            for rating in ratings:
                product_page.rating_checkbox(rating)            
            assert product_page.is_only_filtered_ratings(ratings), "Rating filter does not work"
            for rating in ratings:
                product_page.rating_checkbox(rating)            
        with step('Filter 1'):
            product_page = ProductPage(browser, browser.current_url)            
            ratings = ['1']
            for rating in ratings:
                product_page.rating_checkbox(rating)            
            assert product_page.is_only_filtered_ratings(ratings), "Rating filter does not work"
            for rating in ratings:
                product_page.rating_checkbox(rating)
        with step('Filter 4 and 2'):
            product_page = ProductPage(browser, browser.current_url)            
            ratings = ['4', '2']
            for rating in ratings:
                product_page.rating_checkbox(rating)            
            assert product_page.is_only_filtered_ratings(ratings), "Rating filter does not work"
            for rating in ratings:
                product_page.rating_checkbox(rating)
